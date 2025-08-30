'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navLinks = [
  { href: '/dashboard', label: 'Dashboard' },
  { href: '/maps', label: 'Maps' },
  { href: '/vessels', label: 'Vessels' },
  { href: '/ai/analysis', label: 'AI Analysis' },
  { href: '/users', label: 'Users' },
];

const Sidebar: React.FC = () => {
  const pathname = usePathname();

  return (
    <aside style={{ width: '250px', background: '#e5e7eb', padding: '1rem' }}>
      <nav>
        <ul>
          {navLinks.map((link) => (
            <li key={link.href} style={{ marginBottom: '0.5rem' }}>
              <Link href={link.href} style={{
                display: 'block',
                padding: '0.5rem',
                borderRadius: '4px',
                textDecoration: 'none',
                color: 'black',
                backgroundColor: pathname === link.href ? '#d1d5db' : 'transparent'
              }}>
                {link.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
