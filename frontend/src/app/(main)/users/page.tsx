'use client';

import React, { useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { api } from '@/lib/api';
import UserForm from '@/components/forms/UserForm';

interface User {
    id: number;
    username: string;
    email: string;
    role: string;
}

const UsersPage: React.FC = () => {
    const { token } = useAuth();
    const [users, setUsers] = useState<User[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const [isFormOpen, setIsFormOpen] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [currentUser, setCurrentUser] = useState<User | null>(null);

    useEffect(() => {
        const fetchUsers = async () => {
            if (!token) {
                setIsLoading(false);
                setError("Authentication token not found.");
                return;
            }

            try {
                const response = await api.get('/users', {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUsers(response.data);
            } catch (err) {
                setError("Failed to fetch users.");
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchUsers();
    }, [token]);

    const handleAddUser = () => {
        setIsEditing(false);
        setCurrentUser(null);
        setIsFormOpen(true);
    };

    const handleEditUser = (user: User) => {
        setIsEditing(true);
        setCurrentUser(user);
        setIsFormOpen(true);
    };

    const handleFormSubmit = async (data: any) => {
        if (!token) {
            alert("Authentication token not found.");
            return;
        }

        const url = isEditing ? `/users/${currentUser?.id}` : '/users';
        const method = isEditing ? 'put' : 'post';

        try {
            const response = await api[method](url, data, {
                headers: { Authorization: `Bearer ${token}` }
            });

            if (isEditing) {
                setUsers(users.map(u => (u.id === currentUser?.id ? response.data : u)));
            } else {
                setUsers([...users, response.data]);
            }
            setIsFormOpen(false);
        } catch (err) {
            alert(`Failed to ${isEditing ? 'update' : 'create'} user.`);
            console.error(err);
        }
    };

    const handleDeleteUser = async (id: number) => {
        if (!token) {
            alert("Authentication token not found.");
            return;
        }
        if (confirm('Are you sure you want to delete this user?')) {
            try {
                await api.delete(`/users/${id}`, {
                    headers: { Authorization: `Bearer ${token}` }
                });
                setUsers(users.filter(user => user.id !== id));
            } catch (err) {
                alert("Failed to delete user.");
                console.error(err);
            }
        }
    };


    if (isLoading) return <div>Loading users...</div>;
    if (error) return <div>Error: {error}</div>;

    return (
        <div>
            {isFormOpen && (
                <UserForm
                    user={currentUser}
                    onSubmit={handleFormSubmit}
                    onCancel={() => setIsFormOpen(false)}
                    isEditing={isEditing}
                />
            )}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>User Management</h1>
                <button onClick={handleAddUser} style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>
                    Add User
                </button>
            </div>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                    <tr>
                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>ID</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Username</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Email</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Role</th>
                        <th style={{ border: '1px solid #ddd', padding: '8px', textAlign: 'left' }}>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {users.map((user) => (
                        <tr key={user.id}>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{user.id}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{user.username}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{user.email}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>{user.role}</td>
                            <td style={{ border: '1px solid #ddd', padding: '8px' }}>
                                <button onClick={() => handleEditUser(user)} style={{ marginRight: '0.5rem' }}>Edit</button>
                                <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default UsersPage;
