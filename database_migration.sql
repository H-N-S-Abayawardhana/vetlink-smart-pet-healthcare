-- VetLink Role-Based Authentication Database Migration
-- Run these queries in your PostgreSQL database to add user roles

-- Step 1: Create the enum type for user roles
CREATE TYPE user_role_enum AS ENUM ('SUPER_ADMIN', 'VETERINARIAN', 'USER');

-- Step 2: Add the user_role column to the users table
ALTER TABLE users 
ADD COLUMN user_role user_role_enum DEFAULT 'USER' NOT NULL;

-- Step 3: Add an index on user_role for better query performance
CREATE INDEX idx_users_user_role ON users(user_role);

-- Step 4: Update existing users to have 'USER' role (this is already the default, but explicit for clarity)
UPDATE users SET user_role = 'USER' WHERE user_role IS NULL;

-- Step 5: Verify the changes
SELECT 
    id, 
    username, 
    email, 
    user_role, 
    is_active, 
    created_at 
FROM users 
ORDER BY created_at DESC 
LIMIT 10;

-- Optional: Create a super admin user (replace with your desired credentials)
-- INSERT INTO users (username, email, password_hash, user_role, is_active, created_at, updated_at)
-- VALUES (
--     'admin', 
--     'admin@vetlink.com', 
--     '$2a$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Kz8KzK', -- This is 'admin123' hashed
--     'SUPER_ADMIN', 
--     true, 
--     CURRENT_TIMESTAMP, 
--     CURRENT_TIMESTAMP
-- );

-- Verify the migration was successful
SELECT 
    'Migration completed successfully' as status,
    COUNT(*) as total_users,
    COUNT(CASE WHEN user_role = 'USER' THEN 1 END) as user_count,
    COUNT(CASE WHEN user_role = 'VETERINARIAN' THEN 1 END) as veterinarian_count,
    COUNT(CASE WHEN user_role = 'SUPER_ADMIN' THEN 1 END) as super_admin_count
FROM users;
