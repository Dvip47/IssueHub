import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const Signup = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [error, setError] = useState('');
    const { signup } = useAuth();
    const navigate   = useNavigate();



    const handleSubmit = async e => {
        e.preventDefault()

        const ok = await signup(email, password, name)

        if (ok) {
            navigate('/projects')
        } else {
            setError('Signup failed. Email might be taken.')
        }
    }

    return (
        <div className="auth-form card">

            <h2>Join issueHub</h2>

            {error && (
                <div style={{ color: 'red' }}>
                    {error}
                </div>
            )}

            <form onSubmit={handleSubmit}>
                <div>
                    <label>Name</label>
                    <input
                        required
                        type="text"
                        value={name}
                        onChange={e => setName(e.target.value)}
                    />
                </div>

                <div>
                    <label>Email</label>
                    <input
                        required
                        type="email"
                        value={email}
                        onChange={e => setEmail(e.target.value)}
                    />
                </div>

                <div>
                    <label>Password</label>
                    <input
                        required
                        type="password"
                        value={password}
                        onChange={e => setPassword(e.target.value)}
                    />
                </div>

                <button
                    type="submit"
                    className="btn btn-primary"
                    style={{ width: '100%' }}
                >
                    Sign Up
                </button>
            </form>

            <p style={{ marginTop: 10 }}>
                Already have an account? <Link to="/login">Login</Link>
            </p>
        </div>
    )
}

export default Signup
