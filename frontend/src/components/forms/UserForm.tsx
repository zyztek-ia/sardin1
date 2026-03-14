'use client';

import React, { useState, useEffect } from 'react';

interface UserFormData {
    username: string;
    email: string;
    role: string;
    password?: string;
}

interface UserFormProps {
    user?: UserFormData | null;
    onSubmit: (data: UserFormData) => void;
    onCancel: () => void;
    isEditing: boolean;
}

const UserForm: React.FC<UserFormProps> = ({ user, onSubmit, onCancel, isEditing }) => {
    const [formData, setFormData] = useState<UserFormData>({
        username: '',
        email: '',
        role: 'user',
        password: ''
    });

    useEffect(() => {
        if (isEditing && user) {
            setFormData({
                username: user.username,
                email: user.email,
                role: user.role,
                password: ''
            });
        }
    }, [user, isEditing]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        const dataToSubmit = { ...formData };
        if (!isEditing && !dataToSubmit.password) {
            alert("Password is required for new users.");
            return;
        }
        onSubmit(dataToSubmit);
    };

    return (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', backgroundColor: 'rgba(0,0,0,0.5)', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <form onSubmit={handleSubmit} style={{ background: 'white', padding: '2rem', borderRadius: '8px', width: '400px' }}>
                <h2>{isEditing ? 'Edit User' : 'Add User'}</h2>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Username</label>
                    <input type="text" name="username" value={formData.username} onChange={handleChange} required style={{ width: '100%', padding: '0.5rem' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Email</label>
                    <input type="email" name="email" value={formData.email} onChange={handleChange} required style={{ width: '100%', padding: '0.5rem' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Password ({isEditing ? "leave blank to keep current" : "required"})</label>
                    <input type="password" name="password" value={formData.password} onChange={handleChange} style={{ width: '100%', padding: '0.5rem' }} />
                </div>
                <div style={{ marginBottom: '1rem' }}>
                    <label>Role</label>
                    <select name="role" value={formData.role} onChange={handleChange} style={{ width: '100%', padding: '0.5rem' }}>
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                    </select>
                </div>
                <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
                    <button type="button" onClick={onCancel} style={{ marginRight: '1rem' }}>Cancel</button>
                    <button type="submit">{isEditing ? 'Update' : 'Create'}</button>
                </div>
            </form>
        </div>
    );
};

export default UserForm;
