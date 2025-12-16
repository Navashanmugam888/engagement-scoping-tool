'use client';
import React, { useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link'; // <--- Added Link Import
import { signIn } from 'next-auth/react';
import { Button } from 'primereact/button';
import { InputText } from 'primereact/inputtext';
import { Checkbox } from 'primereact/checkbox';
import { Divider } from 'primereact/divider';
import { Toast } from 'primereact/toast';
import Image from 'next/image';
import { EyeIcon, EyeOffIcon } from 'lucide-react';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const [rememberMe, setRememberMe] = useState(false);
    const [emailLoading, setEmailLoading] = useState(false);
    const [ssoLoading, setSsoLoading] = useState(false);
    const router = useRouter();
    const toast = useRef(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setEmailLoading(true);
        try {
            const result = await signIn('credentials', {
                redirect: false, // Prevent auto-redirect to handle errors manually
                email,
                password,
            });

            if (result?.error) {
                toast.current.show({
                    severity: 'error',
                    summary: 'Login Failed',
                    detail: 'Invalid credentials or account is pending approval.',
                });
                setEmailLoading(false);
            } else if (result?.ok) {
                 // Successful login
                 // Redirect based on role - will be handled by middleware
                 router.push('/fccs-scoping');
            }
        } catch (error) {
            toast.current.show({
                severity: 'error',
                summary: 'Error',
                detail: 'Could not connect to server.',
            });
            setEmailLoading(false);
        }
    };

    const handleSSOLogin = async () => {
        setSsoLoading(true);
        await signIn('azure-ad', { callbackUrl: '/fccs-scoping' });
    };

    // Right-side feature card component
    const FeatureCardBlue = ({ icon, title, children }) => (
        <div className="flex items-start p-4 bg-gray-800/80 backdrop-blur-sm rounded-xl border border-gray-700 shadow-sm hover:shadow-blue-500/10 transition-shadow duration-300">
            <div className="flex-shrink-0 w-10 h-10 rounded-lg bg-blue-600/10 flex items-center justify-center border border-blue-500/30">
                <i className={`pi ${icon} text-blue-400 text-lg`}></i>
            </div>
            <div className="ml-4">
                <h3 className="font-semibold text-white">{title}</h3>
                <p className="text-sm text-gray-400 mt-1">{children}</p>
            </div>
        </div>
    );

    return (
        <>
            <Toast ref={toast} />
            <div className="min-h-screen flex">
                {/* LEFT SIDE - LOGIN FORM */}
                <div className="w-full md:w-1/2 lg:w-5/12 bg-white flex flex-col justify-center p-10 sm:p-14">
                    <div className="w-full max-w-md mx-auto">
                        {/* Logo and Header */}
                        <div className="mb-10 text-center">
                            <div className="flex justify-center mb-6">
                                <Image
                                    src="/mlogo.png"
                                    alt="MaestroAI Logo"
                                    width={220}
                                    height={80}
                                    className="object-contain"
                                    unoptimized
                                />
                            </div>
                            <h1 className="text-4xl font-bold text-[#4B2E83] mb-2">
                                Welcome back
                            </h1>
                            <p className="text-gray-600 text-sm">
                                Please sign in to access your account.
                            </p>
                        </div>

                        {/* Email and Password Form */}
                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">Email *</label>
                                <InputText
                                    id="email"
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    type="email"
                                    required
                                    placeholder="you@company.com"
                                    className="w-full rounded-lg focus:ring-2 focus:ring-[#7AC943] focus:border-[#7AC943] transition"
                                />
                            </div>

                            <div>
                                <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">Password *</label>
                                <div className="relative">
                                    <InputText
                                        id="password"
                                        type={showPassword ? 'text' : 'password'}
                                        value={password}
                                        onChange={(e) => setPassword(e.target.value)}
                                        required
                                        placeholder="Enter your password"
                                        className="w-full pr-10 rounded-lg focus:ring-2 focus:ring-[#7AC943] focus:border-[#7AC943] transition"
                                    />
                                    <button
                                        type="button"
                                        onClick={() => setShowPassword(!showPassword)}
                                        className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-[#4B2E83] focus:outline-none"
                                        tabIndex={-1}
                                    >
                                        {showPassword ? <EyeOffIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                                    </button>
                                </div>
                            </div>

                            <div className="flex items-center justify-between">
                                <div className="flex items-center">
                                    <Checkbox
                                        inputId="rememberMe"
                                        checked={rememberMe}
                                        onChange={(e) => setRememberMe(e.checked)}
                                    />
                                    <label htmlFor="rememberMe" className="ml-2 text-sm text-gray-700">Remember me</label>
                                </div>
                                <a href="#" className="text-sm font-medium text-[#4B2E83] hover:text-[#7AC943] transition-colors">
                                    Forgot Password?
                                </a>
                            </div>

                            <Button
                                type="submit"
                                label={emailLoading ? 'Signing in...' : 'Login'}
                                className="w-full !bg-[#7AC943] !border-none !text-white font-semibold py-3 rounded-lg hover:!bg-[#6AB038] focus:!ring-2 focus:!ring-[#4B2E83] transition-all duration-200 shadow-sm hover:shadow-md"
                                loading={emailLoading}
                                disabled={emailLoading || ssoLoading}
                            />
                        </form>

                        <Divider align="center" className="my-6">
                            <span className="text-sm text-gray-500">or</span>
                        </Divider>

                        <div className="mb-6">
                            <Button
                                label="Log in with Azure SSO"
                                icon="pi pi-microsoft"
                                className="w-full !bg-[#4B2E83] !border-none !text-white hover:!bg-[#3B286D] focus:!ring-2 focus:!ring-[#7AC943] transition-all duration-200 rounded-lg"
                                onClick={handleSSOLogin}
                                loading={ssoLoading}
                                disabled={emailLoading || ssoLoading}
                            />
                        </div>

                        <div className="text-center text-sm text-gray-600 mt-8">
                            Donâ€™t have an account?
                            {/* FIXED: Using Link to navigate to signup */}
                            <Link 
                                href="/signup" 
                                className="font-medium text-[#4B2E83] hover:text-[#7AC943] ml-1 transition"
                            >
                                Sign up
                            </Link>
                        </div>
                    </div>
                </div>

                {/* RIGHT SIDE - INFO SECTION */}
                <div className="hidden md:block md:w-1/2 lg:w-7/12 bg-gray-900 p-12 lg:p-20 relative overflow-hidden">
                    <div className="max-w-md mx-auto flex flex-col justify-center h-full">
                        <div className="space-y-6">
                            <h2 className="text-3xl font-semibold text-white leading-snug">
                                Unlock Actionable <br />
                                <span className="text-blue-400">Company Insights</span>
                            </h2>
                            <p className="text-lg text-gray-400">
                                Log in to access your dashboard, analyze company performance, and discover new opportunities.
                            </p>
                            <div className="space-y-4 pt-4">
                                <FeatureCardBlue icon="pi-chart-line" title="Performance Analysis">
                                    Visualize revenue, performance, and growth metrics.
                                </FeatureCardBlue>
                                <FeatureCardBlue icon="pi-desktop" title="Technology Tracking">
                                    Identify key technology platforms and adoption rates.
                                </FeatureCardBlue>
                                <FeatureCardBlue icon="pi-users" title="Leadership Access">
                                    Track contact counts and leadership access scores.
                                </FeatureCardBlue>
                            </div>
                        </div>
                        <div className="text-center mt-12 text-gray-500 text-sm absolute bottom-12 left-0 right-0">
                            &copy; 2025 MaestroAI. All rights reserved.
                        </div>
                    </div>
                    <div className="absolute top-0 -left-20 w-72 h-72 bg-blue-500/10 rounded-full blur-3xl"></div>
                    <div className="absolute bottom-0 -right-20 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl"></div>
                </div>
            </div>
        </>
    );
}
