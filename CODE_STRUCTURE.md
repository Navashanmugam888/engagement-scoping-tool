# Frontend Code Structure Documentation

## Overview
This document outlines the professional code structure implemented for the Admin Scoping Application. The new architecture follows industry best practices for scalability, maintainability, and reusability.

## Directory Structure

```
app/(app)/
├── constants/          # Application-wide constants
│   ├── roles.js       # Role definitions and configurations
│   ├── status.js      # Status definitions and configurations
│   └── theme.js       # Theme colors and button styles
│
├── components/
│   ├── common/        # Reusable UI components
│   │   ├── Button.jsx
│   │   ├── PageHeader.jsx
│   │   ├── UserAvatar.jsx
│   │   ├── RoleBadge.jsx
│   │   └── StatusBadge.jsx
│   │
│   └── admin/         # Admin-specific components
│       ├── UserDialog.jsx
│       └── UserTable.jsx
│
├── hooks/             # Custom React hooks
│   ├── useAuth.js
│   ├── useToast.js
│   └── useUsers.js
│
└── utils/             # Utility functions
    ├── api.js
    ├── formatters.js
    └── validators.js
```

## Component Architecture

### 1. Constants (`/constants`)

#### `roles.js`
Centralized role definitions:
- **ROLES**: Object mapping role keys to values
- **ROLE_OPTIONS**: Array for dropdown components
- **ROLE_CONFIG**: Role metadata (labels, colors)

```javascript
export const ROLES = {
  SUPER_ADMIN: 'SUPER_ADMIN',
  SUPER_USER: 'SUPER_USER',
  // ...
};

export const ROLE_CONFIG = {
  SUPER_ADMIN: { label: 'Administrator', color: '#dc2626' },
  // ...
};
```

#### `status.js`
Centralized status definitions:
- **STATUS**: Object mapping status keys
- **STATUS_OPTIONS**: Array for dropdown components
- **STATUS_CONFIG**: Status metadata (labels, colors)

#### `theme.js`
Centralized theme configuration:
- **COLORS**: Brand color palette
- **BUTTON_STYLES**: Predefined button variants (primary, secondary, outlined)

### 2. Common Components (`/components/common`)

#### `Button.jsx`
Standardized button component with variants:
- **Variants**: primary, secondary, outlined
- **Sizes**: sm, md, lg
- **Props**: label, icon, onClick, variant, size, className, style

```jsx
<Button 
  label="Save" 
  variant="primary" 
  size="md" 
  onClick={handleSave} 
/>
```

#### `PageHeader.jsx`
Consistent page header with title, subtitle, icon, and actions:
```jsx
<PageHeader
  title="Manage Users"
  subtitle="View and manage all system users"
  icon={PeopleOutlinedIcon}
  actions={<Button label="Add User" />}
/>
```

#### `UserAvatar.jsx`
User avatar with initials and customizable sizes:
```jsx
<UserAvatar name="John Doe" size="md" />
```

#### `RoleBadge.jsx`
Colored badge for displaying user roles:
```jsx
<RoleBadge role="SUPER_ADMIN" />
```

#### `StatusBadge.jsx`
Colored badge for displaying user status:
```jsx
<StatusBadge status="ACTIVE" />
```

### 3. Admin Components (`/components/admin`)

#### `UserTable.jsx`
Reusable data table for displaying users:
- Pagination
- Global filtering
- Custom column templates
- Edit/Delete actions

```jsx
<UserTable
  users={users}
  globalFilterValue={searchTerm}
  onEdit={handleEdit}
  onDelete={handleDelete}
/>
```

#### `UserDialog.jsx`
Modal dialog for editing user details:
```jsx
<UserDialog
  visible={showDialog}
  onHide={() => setShowDialog(false)}
  user={selectedUser}
  onChange={handleChange}
  onSave={handleSave}
  title="Edit User"
/>
```

### 4. Custom Hooks (`/hooks`)

#### `useAuth.js`
Authentication and authorization hook:
```javascript
const { 
  user, 
  isAuthenticated, 
  isSuperAdmin,
  canAccessAdmin 
} = useAuth();
```

Features:
- Session management
- Role checking utilities
- Permission helpers

#### `useToast.js`
Toast notification management:
```javascript
const { toastRef, showSuccess, showError } = useToast();

showSuccess('User updated successfully');
showError('Failed to update user');
```

#### `useUsers.js`
User data management hook:
```javascript
const { 
  users, 
  loading, 
  updateUser, 
  deleteUser, 
  refetch 
} = useUsers();
```

Features:
- Automatic data fetching
- CRUD operations
- Loading states
- Error handling

### 5. Utilities (`/utils`)

#### `api.js`
Centralized API request functions:
- `apiRequest()`: Base fetch wrapper with error handling
- `getUsers()`: Fetch all users
- `updateUser()`: Update user data
- `deleteUser()`: Delete user
- `getScopingSubmissions()`: Fetch scoping data

#### `formatters.js`
Data formatting utilities:
- `formatDate()`: Smart date formatting (relative/absolute)
- `formatDateTime()`: Full date-time formatting
- `formatRoleLabel()`: Role label formatter
- `formatStatusLabel()`: Status label formatter
- `formatCurrency()`: Currency formatter
- `formatNumber()`: Number formatter
- `formatPercentage()`: Percentage formatter

#### `validators.js`
Input validation functions:
- `validateEmail()`: Email format validation
- `validateRequired()`: Required field validation
- `validateUserName()`: Username validation with rules
- `validateUserEmail()`: Combined email validation
- `validatePercentage()`: Percentage range validation

## Migration Example

### Before (Monolithic - 459 lines):
```jsx
'use client';
import React, { useState, useEffect, useRef } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
// ... 20+ imports

export default function ManageUsers() {
  // 100+ lines of state management
  // 200+ lines of API logic
  // 150+ lines of component templates
  // All mixed together
}
```

### After (Modular - 125 lines):
```jsx
'use client';
import PageHeader from '../../components/common/PageHeader';
import UserTable from '../../components/admin/UserTable';
import useAuth from '../../hooks/useAuth';
import useUsers from '../../hooks/useUsers';

export default function ManageUsers() {
  const { users, updateUser } = useUsers();
  
  return (
    <div>
      <PageHeader title="Manage Users" />
      <UserTable users={users} onEdit={updateUser} />
    </div>
  );
}
```

## Benefits

### 1. **Reusability**
- Components can be used across multiple pages
- Reduces code duplication by 60-70%
- Consistent UI/UX across the application

### 2. **Maintainability**
- Single source of truth for constants (colors, roles, status)
- Easy to update global styles or behavior
- Clear separation of concerns

### 3. **Testability**
- Each component/hook can be tested independently
- Utilities are pure functions (easy to test)
- Mocked data can be injected easily

### 4. **Scalability**
- New features can be added without modifying existing code
- Components can be extended or composed
- Clear file organization makes it easy to find code

### 5. **Developer Experience**
- Intuitive folder structure
- Self-documenting code with clear naming
- Easier onboarding for new developers

## Usage Guidelines

### When to Create a New Component
- Code is used in 2+ places
- Component has clear single responsibility
- Component is 50+ lines

### When to Create a New Hook
- State logic is reused across components
- Side effects need to be abstracted
- Complex state management needs encapsulation

### When to Create a New Utility
- Function is used in 2+ places
- Function has no side effects (pure function)
- Function provides data transformation/validation

## Next Steps

### Recommended Refactoring Order:
1. ✅ **Constants** - Completed
2. ✅ **Common Components** - Completed
3. ✅ **Admin Components** - Completed
4. ✅ **Hooks** - Completed
5. ✅ **Utilities** - Completed
6. ⏳ **Refactor Pages** - In Progress
   - Start with `/admin/users/page.jsx` (example created as `page-refactored.jsx`)
   - Then `/admin/role-allocations/page.jsx`
   - Then `/dashboard/page.js`
   - Then `/scoping-history/page.jsx`

### Testing the Refactored Code:
1. Review `page-refactored.jsx` side-by-side with original `page.jsx`
2. Test all functionality (edit, delete, search)
3. Once verified, replace `page.jsx` with `page-refactored.jsx`
4. Repeat for other pages

## File Comparison

### Original: `/admin/users/page.jsx`
- **Lines**: 459
- **Imports**: 13
- **State Variables**: 7
- **Functions**: 12
- **Template Functions**: 5

### Refactored: `/admin/users/page-refactored.jsx`
- **Lines**: 125 (73% reduction)
- **Imports**: 10
- **State Variables**: 4
- **Functions**: 4
- **External Components**: 5
- **External Hooks**: 3

## Color System

### Status Colors (Light Background + Dark Text):
- **ACTIVE**: `#dcfce7` background, `#166534` text
- **INACTIVE**: `#fee2e2` background, `#991b1b` text
- **PENDING**: `#fef9c3` background, `#854d0e` text

### Role Colors:
- **SUPER_ADMIN**: `#dc2626` (Red)
- **SUPER_USER**: `#ea580c` (Orange)
- **HISTORY_VIEWER**: `#2563eb` (Blue)
- **SCOPING_EDITOR**: `#16a34a` (Green)
- **GUEST**: `#6b7280` (Gray)

### Button Styles:
- **Primary**: Purple background (`#2d1b4e`), white text
- **Secondary**: Gray background, white text
- **Outlined**: White background, purple border and text

All defined in `/constants/theme.js`
