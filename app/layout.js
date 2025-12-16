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
      <body className={`${inter.className} bg-gray-100 font-sans`}>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  );
}