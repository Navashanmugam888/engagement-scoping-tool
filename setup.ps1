# Admin & Scoping App Setup Script
# This script copies and adapts files from the main sales dashboard project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Admin & Scoping App Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$SourceProject = "..\app"
$TargetProject = "."

# Check if source project exists
if (-not (Test-Path $SourceProject)) {
    Write-Host "ERROR: Source project not found at $SourceProject" -ForegroundColor Red
    exit 1
}

Write-Host "Step 1: Creating folder structure..." -ForegroundColor Yellow

# Create app directory structure
$folders = @(
    "app\(app)\admin\users",
    "app\(app)\fccs-scoping",
    "app\(app)\components\Header",
    "app\(app)\components\Sidebar",
    "app\(app)\components\Loader",
    "app\(app)\components\SubLayout",
    "app\(auth)",
    "app\access-pending",
    "app\api\admin\users",
    "app\api\auth\[...nextauth]",
    "app\lib",
    "public"
)

foreach ($folder in $folders) {
    $path = Join-Path $TargetProject $folder
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "  Created: $folder" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 2: Copying configuration files..." -ForegroundColor Yellow

# Copy config files
$configFiles = @(
    "tailwind.config.js",
    "postcss.config.mjs",
    "components.json",
    "jsconfig.json"
)

foreach ($file in $configFiles) {
    $source = Join-Path $SourceProject $file
    $dest = Join-Path $TargetProject $file
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Force
        Write-Host "  Copied: $file" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 3: Copying styles..." -ForegroundColor Yellow

# Copy styles
Copy-Item -Path "$SourceProject\app\globals.css" -Destination "$TargetProject\app\globals.css" -Force
Write-Host "  Copied: app\globals.css" -ForegroundColor Green

Write-Host ""
Write-Host "Step 4: Copying library files..." -ForegroundColor Yellow

# Copy lib files
Copy-Item -Path "$SourceProject\app\lib\db.js" -Destination "$TargetProject\app\lib\db.js" -Force
Write-Host "  Copied: app\lib\db.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 5: Copying authentication..." -ForegroundColor Yellow

# Copy NextAuth route
Copy-Item -Path "$SourceProject\app\api\auth\[...nextauth]\route.js" -Destination "$TargetProject\app\api\auth\[...nextauth]\route.js" -Force
Write-Host "  Copied: app\api\auth\[...nextauth]\route.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 6: Copying feature pages..." -ForegroundColor Yellow

# Copy fccs-scoping pages
Copy-Item -Path "$SourceProject\app\(app)\fccs-scoping\*" -Destination "$TargetProject\app\(app)\fccs-scoping\" -Recurse -Force
Write-Host "  Copied: fccs-scoping folder" -ForegroundColor Green

# Copy admin pages
Copy-Item -Path "$SourceProject\app\(app)\admin\users\*" -Destination "$TargetProject\app\(app)\admin\users\" -Recurse -Force
Write-Host "  Copied: admin\users folder" -ForegroundColor Green

# Copy admin API
Copy-Item -Path "$SourceProject\app\api\admin\users\*" -Destination "$TargetProject\app\api\admin\users\" -Recurse -Force
Write-Host "  Copied: api\admin\users folder" -ForegroundColor Green

# Copy access-pending
Copy-Item -Path "$SourceProject\app\access-pending\page.js" -Destination "$TargetProject\app\access-pending\page.js" -Force
Write-Host "  Copied: access-pending\page.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 7: Copying auth pages..." -ForegroundColor Yellow

# Copy auth pages
Copy-Item -Path "$SourceProject\app\(auth)\page.js" -Destination "$TargetProject\app\(auth)\page.js" -Force
Copy-Item -Path "$SourceProject\app\(auth)\layout.js" -Destination "$TargetProject\app\(auth)\layout.js" -Force
Write-Host "  Copied: auth pages" -ForegroundColor Green

Write-Host ""
Write-Host "Step 8: Copying UI components..." -ForegroundColor Yellow

# Copy components
$components = @(
    "Loader\Loader.js",
    "SubLayout\SubLayout.js"
)

foreach ($comp in $components) {
    $source = Join-Path "$SourceProject\app\(app)\components" $comp
    $dest = Join-Path "$TargetProject\app\(app)\components" $comp
    Copy-Item -Path $source -Destination $dest -Force
    Write-Host "  Copied: components\$comp" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 9: Copying and modifying Sidebar..." -ForegroundColor Yellow

# Copy and modify Sidebar - remove Dashboard link, keep only Scoping & Admin
$sidebarContent = Get-Content "$SourceProject\app\(app)\components\Sidebar\Sidebar.js" -Raw

# Remove Dashboard section from items array
$sidebarContent = $sidebarContent -replace "(?s)// 1\. Dashboard.*?\}\);", ""
# Keep Scoping and Admin sections intact

Set-Content -Path "$TargetProject\app\(app)\components\Sidebar\Sidebar.js" -Value $sidebarContent
Write-Host "  Modified and copied: Sidebar.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 10: Copying and modifying Header..." -ForegroundColor Yellow

# Copy and modify Header - remove dashboard features
$headerContent = Get-Content "$SourceProject\app\(app)\components\Header\Header.js" -Raw

# Remove DataContext import and usage
$headerContent = $headerContent -replace "import \{ useData \} from '@/app/context/DataContext';", ""
$headerContent = $headerContent -replace "import Papa from 'papaparse';", ""
$headerContent = $headerContent -replace "const \{ appendCompanies, clearData, setActiveView, allCompanies \} = useData\(\);", ""

# Remove dashboard-specific state and functions
$headerContent = $headerContent -replace "const \[isUploadVisible, setIsUploadVisible\] = useState\(false\);", ""
$headerContent = $headerContent -replace "const \[selectedFile, setSelectedFile\] = useState\(null\);", ""
$headerContent = $headerContent -replace "const \[sources, setSources\] = useState\(\['ZoomInfo'\]\);", ""
$headerContent = $headerContent -replace "const \[isUploading, setIsUploading\] = useState\(false\);", ""
$headerContent = $headerContent -replace "const fileUploadRef = useRef\(null\);", ""

# Simplify visibility logic - only keep download for scoping
$headerContent = $headerContent -replace "const showLoadClear = isDashboard && \(isSuperAdmin \|\| isSalesUser\);", ""
$headerContent = $headerContent -replace "const showDownload = \(isDashboard \|\| isScoping\) && \(isSuperAdmin \|\| isFccsManager \|\| isSalesUser\);", "const showDownload = isScoping && (isSuperAdmin || isFccsManager);"

# Remove Load/Clear button JSX
$headerContent = $headerContent -replace "(?s)\{/\* --- LOAD & CLEAR BUTTONS.*?\}\)", ""

# Remove Upload Dialog
$headerContent = $headerContent -replace "(?s)\{/\* UPLOAD DIALOG \*/\}.*$", ""

Set-Content -Path "$TargetProject\app\(app)\components\Header\Header.js" -Value $headerContent
Write-Host "  Modified and copied: Header.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 11: Copying middleware and modifying..." -ForegroundColor Yellow

# Copy and modify middleware - remove dashboard routes
$middlewareContent = Get-Content "$SourceProject\middleware.js" -Raw

# Update matcher to remove dashboard, companies, etc.
$newMatcher = @"
export const config = {
    matcher: [
        // Protect admin and scoping routes only
        '/admin/:path*',
        '/fccs-scoping/:path*',
        '/access-pending', 
    ],
};
"@

$middlewareContent = $middlewareContent -replace "(?s)export const config = \{.*?\};", $newMatcher

# Update SALES_USER restriction - they have no access to this app
$middlewareContent = $middlewareContent -replace "// --- 2\. SALES USER RESTRICTIONS ---.*?if \(userRole === 'SALES_USER'\) \{.*?\}", @"
// --- 2. SALES USER - NO ACCESS TO THIS APP ---
        if (userRole === 'SALES_USER') {
            // Sales users should use the main dashboard app, not this one
            return NextResponse.redirect(new URL('/access-pending', req.url));
        }
"@

Set-Content -Path "$TargetProject\middleware.js" -Value $middlewareContent
Write-Host "  Modified and copied: middleware.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 12: Copying .env and updating port..." -ForegroundColor Yellow

# Copy .env and update NEXTAUTH_URL
if (Test-Path "$SourceProject\.env") {
    $envContent = Get-Content "$SourceProject\.env" -Raw
    $envContent = $envContent -replace "NEXTAUTH_URL=http://localhost:3000", "NEXTAUTH_URL=http://localhost:3001"
    $envContent = $envContent -replace "# NEXTAUTH_URL=https://lively-ground.*", "# NEXTAUTH_URL=https://admin.yourdomain.com"
    Set-Content -Path "$TargetProject\.env" -Value $envContent
    Write-Host "  Copied and updated: .env (port changed to 3001)" -ForegroundColor Green
} else {
    Write-Host "  WARNING: .env not found in source project" -ForegroundColor Red
}

Write-Host ""
Write-Host "Step 13: Copying public assets..." -ForegroundColor Yellow

# Copy logo
if (Test-Path "$SourceProject\public\mlogo.png") {
    Copy-Item -Path "$SourceProject\public\mlogo.png" -Destination "$TargetProject\public\mlogo.png" -Force
    Write-Host "  Copied: mlogo.png" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 14: Creating layout files..." -ForegroundColor Yellow

# Create app/providers.jsx
$providersContent = @"
'use client';
import { SessionProvider } from 'next-auth/react';

export default function Providers({ children }) {
    return (
        <SessionProvider>
            {children}
        </SessionProvider>
    );
}
"@
Set-Content -Path "$TargetProject\app\providers.jsx" -Value $providersContent
Write-Host "  Created: app\providers.jsx" -ForegroundColor Green

# Create app/layout.js
$rootLayoutContent = @"
'use client';
import Providers from './providers';
import { Inter } from 'next/font/google';
import 'primereact/resources/themes/lara-light-indigo/theme.css';
import 'primeicons/primeicons.css';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={\`\${inter.className} bg-gray-100 font-sans\`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}
"@
Set-Content -Path "$TargetProject\app\layout.js" -Value $rootLayoutContent
Write-Host "  Created: app\layout.js" -ForegroundColor Green

# Create app/(app)/layout.js
$appLayoutContent = @"
'use client';
import Sidebar from '@/app/(app)/components/Sidebar/Sidebar';
import Header from '@/app/(app)/components/Header/Header';
import SubLayout from '@/app/(app)/components/SubLayout/SubLayout';
import PageLoader from '@/app/(app)/components/Loader/Loader';

export default function AppLayout({ children }) {
  return (
    <>
      <PageLoader />
      <Sidebar />
      <div className="flex flex-col min-h-screen ml-16 transition-all duration-300">
        <Header />
        <SubLayout>{children}</SubLayout>
      </div>
    </>
  );
}
"@
Set-Content -Path "$TargetProject\app\(app)\layout.js" -Value $appLayoutContent
Write-Host "  Created: app\(app)\layout.js" -ForegroundColor Green

Write-Host ""
Write-Host "Step 15: Installing dependencies..." -ForegroundColor Yellow
Write-Host "  This may take a few minutes..." -ForegroundColor Gray

npm install

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Review the copied files" -ForegroundColor White
Write-Host "  2. Run 'npm run dev' to start on port 3001" -ForegroundColor White
Write-Host "  3. Test login with FCCS_MANAGER or SUPER_ADMIN roles" -ForegroundColor White
Write-Host ""
Write-Host "Both apps can run simultaneously:" -ForegroundColor Cyan
Write-Host "  - Sales Dashboard: http://localhost:3000" -ForegroundColor White
Write-Host "  - Admin & Scoping: http://localhost:3001" -ForegroundColor White
Write-Host ""
