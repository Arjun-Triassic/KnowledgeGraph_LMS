-- Bootstrap script to create the first admin user
-- Run this with: psql -U kg_user -d knowledgegraph_lms -f bootstrap_admin.sql

-- Insert the first admin user
INSERT INTO "user" (email, first_name, last_name, role, created_at)
VALUES ('admin@example.com', 'Admin', 'User', 'admin', NOW())
RETURNING id, email, first_name, last_name, role;

-- This will output the user ID - use this ID in the X-User-Id header

