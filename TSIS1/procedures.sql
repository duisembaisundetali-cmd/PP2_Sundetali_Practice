-- Procedure: add_phone - adds a new phone number to an existing contact
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
AS $$
DECLARE
    v_contact_id INTEGER;
BEGIN
    -- Get contact ID
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Insert new phone
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_contact_id, p_phone, p_type);
    
    RAISE NOTICE 'Phone added successfully to contact %', p_contact_name;
END;
$$ LANGUAGE plpgsql;

-- Procedure: move_to_group - moves contact to a group (creates group if needed)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Get or create group
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    IF v_group_id IS NULL THEN
        INSERT INTO groups (name) VALUES (p_group_name)
        RETURNING id INTO v_group_id;
        RAISE NOTICE 'Created new group: %', p_group_name;
    END IF;
    
    -- Get contact ID
    SELECT id INTO v_contact_id FROM contacts WHERE name = p_contact_name;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    
    -- Update contact's group
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    
    RAISE NOTICE 'Contact % moved to group %', p_contact_name, p_group_name;
END;
$$ LANGUAGE plpgsql;

-- Function: search_contacts - searches across name, email, and all phone numbers
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
) AS
$$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(DISTINCT p.phone || ' (' || p.type || ')', ', ') AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE 
        c.name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name
    ORDER BY c.name;
END;
$$ LANGUAGE plpgsql;

-- Function: get_paginated_contacts (with sorting)
CREATE OR REPLACE FUNCTION get_paginated_contacts(
    p_limit INT,
    p_offset INT,
    p_sort_by VARCHAR DEFAULT 'name',
    p_group_filter VARCHAR DEFAULT NULL
)
RETURNS TABLE(
    id INTEGER,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phones TEXT,
    created_at TIMESTAMP
) AS
$$
BEGIN
    RETURN QUERY
    SELECT 
        c.id,
        c.name,
        c.email,
        c.birthday,
        g.name AS group_name,
        STRING_AGG(DISTINCT p.phone || ' (' || p.type || ')', ', ') AS phones,
        c.created_at
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE (p_group_filter IS NULL OR g.name = p_group_filter)
    GROUP BY c.id, g.name
    ORDER BY
        CASE WHEN p_sort_by = 'name' THEN c.name END ASC,
        CASE WHEN p_sort_by = 'birthday' THEN c.birthday END ASC NULLS LAST,
        CASE WHEN p_sort_by = 'created_at' THEN c.created_at END ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Procedure: insert_contact (with upsert for CSV import)
CREATE OR REPLACE PROCEDURE insert_contact(
    p_name VARCHAR,
    p_email VARCHAR DEFAULT NULL,
    p_birthday DATE DEFAULT NULL,
    p_group_name VARCHAR DEFAULT NULL,
    p_phone VARCHAR DEFAULT NULL,
    p_phone_type VARCHAR DEFAULT 'mobile'
)
AS $$
DECLARE
    v_group_id INTEGER;
    v_contact_id INTEGER;
BEGIN
    -- Get or create group
    IF p_group_name IS NOT NULL THEN
        SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
        IF v_group_id IS NULL THEN
            INSERT INTO groups (name) VALUES (p_group_name) RETURNING id INTO v_group_id;
        END IF;
    END IF;
    
    -- Insert contact (handle duplicate)
    INSERT INTO contacts (name, email, birthday, group_id)
    VALUES (p_name, p_email, p_birthday, v_group_id)
    ON CONFLICT (name) DO UPDATE
    SET email = EXCLUDED.email,
        birthday = EXCLUDED.birthday,
        group_id = EXCLUDED.group_id
    RETURNING id INTO v_contact_id;
    
    -- Add phone if provided
    IF p_phone IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type)
        VALUES (v_contact_id, p_phone, p_phone_type)
        ON CONFLICT DO NOTHING;
    END IF;
END;
$$ LANGUAGE plpgsql;