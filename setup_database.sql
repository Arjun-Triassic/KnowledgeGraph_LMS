-- Database setup script for KnowledgeGraph LMS
-- Run with: psql -U postgres -f setup_database.sql

-- Create database
CREATE DATABASE knowledgegraph_lms;

-- Create user
CREATE USER kg_user WITH PASSWORD 'kg_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE knowledgegraph_lms TO kg_user;

-- Allow user to create databases (useful for testing)
ALTER USER kg_user CREATEDB;

-- Connect to the new database and grant schema privileges
\c knowledgegraph_lms

-- Grant schema privileges (for future tables)
GRANT ALL ON SCHEMA public TO kg_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kg_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO kg_user;

-- Display success message
\echo 'Database and user created successfully!'
\echo 'Database: knowledgegraph_lms'
\echo 'User: kg_user'
\echo 'Password: kg_password'

