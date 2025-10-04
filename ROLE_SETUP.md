# Role-Based Authentication Setup

This document explains how to set up and use the role-based authentication system in VetLink.

## Database Setup

### 1. Run the Database Migration

First, you need to add the `user_role` column to your database. Run the following SQL commands:

```sql
-- Create the enum type for user roles
CREATE TYPE user_role_enum AS ENUM ('SUPER_ADMIN', 'VETERINARIAN', 'USER');

-- Add the user_role column to the users table
ALTER TABLE users 
ADD COLUMN user_role user_role_enum DEFAULT 'USER' NOT NULL;

-- Add an index on user_role for better query performance
CREATE INDEX idx_users_user_role ON users(user_role);

-- Update existing users to have 'USER' role
UPDATE users SET user_role = 'USER' WHERE user_role IS NULL;
```

### 2. Create a Super Admin User

Run the following script to create a super admin user:

```bash
node scripts/create-super-admin.js
```

This will create a super admin user with:
- Username: `admin`
- Email: `admin@vetlink.com`
- Password: `admin123`
- Role: `SUPER_ADMIN`

**⚠️ Important: Change the password after first login!**

## User Roles and Permissions

### SUPER_ADMIN
- **Access**: All routes and features
- **Description**: Full system access
- **Allowed Paths**: All paths (`*`)

### VETERINARIAN
- **Access**: Core veterinary features
- **Description**: Veterinarian access to medical tools
- **Allowed Paths**:
  - `/` (home)
  - `/dashboard`
  - `/dashboard/profile`
  - `/dashboard/skin-disease`

### USER
- **Access**: Basic user features
- **Description**: Basic user access
- **Allowed Paths**:
  - `/` (home)
  - `/dashboard`

## Navigation Menu

The sidebar navigation automatically adjusts based on user role:

- **SUPER_ADMIN**: Sees all menu items
- **VETERINARIAN**: Sees Dashboard, Skin Disease Detection, and Profile
- **USER**: Sees only Dashboard

## Role Management

### Changing User Roles

To change a user's role, update the `user_role` column in the database:

```sql
-- Make a user a veterinarian
UPDATE users SET user_role = 'VETERINARIAN' WHERE email = 'user@example.com';

-- Make a user a super admin
UPDATE users SET user_role = 'SUPER_ADMIN' WHERE email = 'user@example.com';

-- Make a user a regular user
UPDATE users SET user_role = 'USER' WHERE email = 'user@example.com';
```

### Adding New Roles

To add new roles:

1. Update the enum type in the database:
```sql
ALTER TYPE user_role_enum ADD VALUE 'NEW_ROLE';
```

2. Update the TypeScript types in `src/types/next-auth.d.ts`
3. Update the role permissions in `src/lib/rbac.ts`
4. Update the role utilities in `src/lib/role-utils.ts`

## Security Features

### Route Protection

- All dashboard routes are protected by authentication
- Specific routes have role-based access control
- Users are redirected to appropriate pages based on their role

### Session Management

- User roles are stored in the JWT token
- Roles are validated on each request
- Session automatically includes role information

## Testing

### Test Different Roles

1. Create test users with different roles
2. Log in with each user
3. Verify that the sidebar shows appropriate menu items
4. Verify that protected routes redirect appropriately

### Test Access Control

1. Try accessing `/dashboard/profile` as a USER (should be denied)
2. Try accessing `/dashboard/skin-disease` as a USER (should be denied)
3. Verify that VETERINARIAN can access both routes
4. Verify that SUPER_ADMIN can access all routes

## Troubleshooting

### Common Issues

1. **User role not showing in session**: Check that the database migration was run and the user has a role assigned
2. **Access denied errors**: Verify the user's role in the database
3. **Sidebar not updating**: Check that the session is being updated after role changes

### Debug Mode

To debug role-based access, check the browser's developer tools:
1. Go to Application/Storage tab
2. Check the session data in localStorage or cookies
3. Verify that `userRole` is present and correct

## Production Considerations

1. **Change default passwords**: Always change default passwords in production
2. **Role assignment**: Implement a proper admin interface for role management
3. **Audit logging**: Consider adding audit logs for role changes
4. **Rate limiting**: Implement rate limiting for authentication endpoints
5. **Session security**: Use secure session settings in production
