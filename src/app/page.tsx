'use client';
import { useState } from 'react';
import { Button } from "@/components/ui/button";
import Map from '@/components/ui/map'; // Make sure the import path is correct
import { useAuth } from '@/components/AuthContext';

export default function Home() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const { isLoggedIn, logout } = useAuth();

  const handleAuthClick = () => {
    if (isLoggedIn) {
      logout();
    } else {
      setIsAuthOpen(true);
    }
  };

  return (
    <div className="bg-black text-white min-h-screen flex flex-col">
      {/* Navbar */}
      <header className="p-4 bg-black">
        <nav className="max-w-6xl mx-auto flex justify-between items-center">
          <Button variant="ghost" className="text-2xl font-bold text-white hover:text-gray-300">
            TechInnovate
          </Button>
          <ul className="flex space-x-4">
            <li><Button variant="ghost" className="text-white hover:text-gray-300">Home</Button></li>
            <li><Button variant="ghost" className="text-white hover:text-gray-300">About</Button></li>
            <li><Button variant="ghost" className="text-white hover:text-gray-300">Services</Button></li>
            <li><Button variant="ghost" className="text-white hover:text-gray-300">Contact</Button></li>
          </ul>
          <Button 
            variant="outline" 
            className="text-white border-white hover:bg-white hover:text-black bg-transparent"
            onClick={handleAuthClick}
          >
            {isLoggedIn ? 'Logout' : 'Register/Login'}
          </Button>
        </nav>
      </header>

      {/* Map Section */}
      <div className="flex-grow" style={{ height: 'calc(100vh - 64px)' }}>
        <Map />
      </div>
    </div>
  );
}
