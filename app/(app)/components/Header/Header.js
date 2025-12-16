'use client';
import React from 'react';
import { useSession } from 'next-auth/react';
import Image from 'next/image';

const getInitials = (name) => {
    if (!name) return '?';
    const names = name.split(' ');
    if (names.length === 1) return names[0][0].toUpperCase();
    return (names[0][0] + names[names.length - 1][0]).toUpperCase();
};

export default function Header() {
    const { data: session, status } = useSession();

    // Don't render while loading or if not authenticated
    if (status === 'loading') {
        return <header className="fixed top-0 left-0 right-0 bg-white border-b border-gray-200 shadow-sm z-30 px-6 py-4 h-20"></header>;
    }

    if (status === 'unauthenticated') {
        return null;
    }

    const userRole = session?.user?.role;

    return (
        <header className="fixed top-0 left-0 right-0 z-50 flex items-center bg-white shadow px-8 py-2 border-b border-gray-200 h-20">
            
            <div className="flex items-center h-full">
                <Image src="/mlogo.png" alt="MaestroAI Logo" width={280} height={100} priority className="object-contain h-16 w-auto" />
            </div>
            
            <div className="ml-auto flex items-center gap-3">
                
                {/* --- USER PROFILE --- */}
                {status === 'authenticated' && session?.user ? (
                    <div className="flex items-center gap-2 ml-4 pl-4 border-l border-gray-300">
                        <div className="w-10 h-10 rounded-full flex justify-center items-center bg-blue-100 text-blue-700 text-sm font-bold overflow-hidden border border-blue-200 shadow-sm">
                            {session.user.image ? (
                                <img src={session.user.image} alt="Profile" className="w-full h-full object-cover" />
                            ) : (
                                getInitials(session.user.name)
                            )}
                        </div>
                        <div className="flex flex-col">
                            <span className="text-sm font-semibold text-gray-700 leading-none">
                                {session.user.name.split(' ')[0]}
                            </span>
                            <span className="text-xs text-gray-500 leading-none mt-1">
                                {userRole === 'SUPER_ADMIN' ? 'Admin' : userRole?.replace('_', ' ') || 'Guest'}
                            </span>
                        </div>
                    </div>
                ) : (
                    <span className="text-sm text-gray-500 ml-4">Not signed in</span>
                )}
            </div>
        </header>
    );
}

