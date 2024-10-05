"use client"

import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"
import { Button } from "@/components/ui/button"
import { useAuth } from '@/components/AuthContext';
import { useRouter } from 'next/navigation';

import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root

const TabsList = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.List>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.List>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props}
  />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Trigger>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Trigger>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow",
      className
    )}
    {...props}
  />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef<
  React.ElementRef<typeof TabsPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof TabsPrimitive.Content>
>(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props}
  />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

// New AuthTabs component
const AuthTabs = () => {
  const [message, setMessage] = React.useState('');
  const { login, checkAuth } = useAuth();
  const router = useRouter();

  const handleAuth = async (event: React.FormEvent<HTMLFormElement>, endpoint: string) => {
    event.preventDefault();
    const form = event.currentTarget;
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    try {
      const response = await fetch(`http://localhost:5000/api/${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
        credentials: 'include',
      });
      const result = await response.json();
      if (response.ok) {
        setMessage(result.message);
        login(); // Call login function to update state
        await checkAuth(); // Check auth status after successful login/register
        router.push('/'); // Redirect to main page
      } else {
        setMessage(result.error || 'An error occurred');
      }
    } catch (error) {
      console.error(`${endpoint} error:`, error);
      setMessage('An error occurred. Please try again.');
    }
  };

  return (
    <Tabs defaultValue="login" className="w-full">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="login">Login</TabsTrigger>
        <TabsTrigger value="register">Register</TabsTrigger>
      </TabsList>
      {message && <div className="mt-4 p-2 bg-blue-100 text-blue-700 rounded">{message}</div>}
      <TabsContent value="login">
        <form className="space-y-4" onSubmit={(e) => handleAuth(e, 'login')}>
          <div className="space-y-2">
            <label htmlFor="login-email" className="block text-sm font-medium">Email</label>
            <input name="email" id="login-email" type="email" placeholder="Enter your email" required className="w-full px-3 py-2 border rounded-md" />
          </div>
          <div className="space-y-2">
            <label htmlFor="login-password" className="block text-sm font-medium">Password</label>
            <input name="password" id="login-password" type="password" placeholder="Enter your password" required className="w-full px-3 py-2 border rounded-md" />
          </div>
          <Button type="submit" className="w-full">Login</Button>
        </form>
      </TabsContent>
      <TabsContent value="register">
        <form className="space-y-4" onSubmit={(e) => handleAuth(e, 'register')}>
          <div className="space-y-2">
            <label htmlFor="register-name" className="block text-sm font-medium">Name</label>
            <input name="name" id="register-name" type="text" placeholder="Enter your name" required className="w-full px-3 py-2 border rounded-md" />
          </div>
          <div className="space-y-2">
            <label htmlFor="register-email" className="block text-sm font-medium">Email</label>
            <input name="email" id="register-email" type="email" placeholder="Enter your email" required className="w-full px-3 py-2 border rounded-md" />
          </div>
          <div className="space-y-2">
            <label htmlFor="register-password" className="block text-sm font-medium">Password</label>
            <input name="password" id="register-password" type="password" placeholder="Create a password" required className="w-full px-3 py-2 border rounded-md" />
          </div>
          <Button type="submit" className="w-full">Register</Button>
        </form>
      </TabsContent>
    </Tabs>
  )
}

export { Tabs, TabsList, TabsTrigger, TabsContent, AuthTabs }
