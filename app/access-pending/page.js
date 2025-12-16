'use client';
import React, { useState } from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { useRouter } from 'next/navigation';
import { useSession, signOut } from 'next-auth/react';

export default function AccessPendingPage() {
    const router = useRouter();
    const { data: session, status, update } = useSession();
    const [checking, setChecking] = useState(false);

    if (status === 'authenticated' && session?.user?.status === 'ACTIVE') {
        router.push('/dashboard');
        return null;
    }

    const handleReturnToLogin = async () => {
        // Sign out to clear the cached session/JWT token
        await signOut({ redirect: true, callbackUrl: '/' });
    };

    const handleRefreshStatus = async () => {
        setChecking(true);
        try {
            // Force session refresh to check if status was updated
            const updatedSession = await update();
            
            // Check if status is now ACTIVE after update
            if (updatedSession?.user?.status === 'ACTIVE') {
                // Status updated! Redirect to dashboard
                router.push('/dashboard');
            } else {
                // Still pending - stay on this page
                setChecking(false);
            }
        } catch (error) {
            console.error('Error refreshing status:', error);
            setChecking(false);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-50 p-6">
            <Card className="w-full max-w-lg text-center shadow-lg border border-gray-200">
                <div className="flex flex-col items-center">
                    <i className="pi pi-clock text-6xl text-yellow-500 mb-4 animate-pulse"></i>
                    <h2 className="text-2xl font-bold text-gray-800 mb-2">Access Pending</h2>
                    <p className="text-lg text-gray-600 mb-6">Thank you for registering! Your account status is currently **PENDING**.</p>
                    <p className="text-sm text-gray-500 mb-8">The administrator needs to approve your access and assign a role before you can use the application. You will be able to log in once your status is set to **ACTIVE**.</p>
                    <div className="flex gap-3 justify-center">
                        <Button 
                            label={checking ? "Checking..." : "Check Status"} 
                            icon={checking ? "pi pi-spin pi-spinner" : "pi pi-refresh"}
                            className="p-button-outlined p-button-primary font-semibold" 
                            onClick={handleRefreshStatus}
                            disabled={checking}
                        />
                        <Button 
                            label="Sign Out" 
                            icon="pi pi-sign-out" 
                            className="p-button-outlined p-button-secondary font-semibold" 
                            onClick={handleReturnToLogin} 
                        />
                    </div>
                </div>
            </Card>
        </div>
    );
}