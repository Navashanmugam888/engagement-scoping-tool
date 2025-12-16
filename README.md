# Admin & Scoping Tool - Separated ProjectThis is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).



This project contains the FCCS Scoping Tool and Admin User Management features, separated from the main Sales Dashboard.## Getting Started



## Quick StartFirst, run the development server:



```bash```bash

# 1. Install dependenciesnpm run dev

npm install# or

yarn dev

# 2. Copy .env from main project and update port# or

# NEXTAUTH_URL=http://localhost:3001pnpm dev

# or

# 3. Run development serverbun dev

npm run dev```

```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

App runs on **http://localhost:3001**

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

## What's Included

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

- **FCCS Scoping Tool** (`/fccs-scoping`) - For `FCCS_MANAGER` and `SUPER_ADMIN`

- **Admin Panel** (`/admin/users`) - For `SUPER_ADMIN` onlyThe `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

- Shared UI components (Header, Sidebar, same design as sales dashboard)

- NextAuth authentication with role-based accessThis project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.



## Setup Checklist## Learn More



I'll help you complete the setup. The following files need to be copied/created:To learn more about Next.js, take a look at the following resources:



### ✅ Already Done- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.

- [x] Created project structure- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

- [x] Set up package.json with correct dependencies

- [x] Configured to run on port 3001You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!



### 📋 TODO (I'll help you with these)## Deploy on Vercel

- [ ] Copy and adapt UI components

- [ ] Copy scoping and admin feature filesThe easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

- [ ] Set up authentication and middleware

- [ ] Create layouts and entry pointsCheck out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

- [ ] Test and verify functionality

## Next Steps

Run these commands in PowerShell to complete setup, or let me know and I'll automate it for you!

