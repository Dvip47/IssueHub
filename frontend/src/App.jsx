import React from 'react'
import {
    BrowserRouter as Router,
    Routes,
    Route,
    Navigate,
    Link
} from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Projects from './pages/Projects'
import ProjectDetail from './pages/ProjectDetail'
import IssueDetail from './pages/IssueDetail'

const ProtectedRoute = ({ children }) => {
    const { user } = useAuth()

    if (!user) return <Navigate to="/login" replace />

    return children
}

const Navbar = () => {
    const { user, logout } = useAuth()
    if (!user) return null

    return (
        <nav className="navbar">
            <div>
                <Link to="/projects">
                    IssueHub
                </Link>
            </div>

            <div>
                <span style={{ marginRight: 15 }}>
                    Hello, {user.name}
                </span>
                <button
                    className="btn btn-secondary"
                    onClick={logout}
                >
                    Logout
                </button>
            </div>
        </nav>
    )
}

function App() {
    return (
        <Router>
            <AuthProvider>
                <Navbar />
                <Routes>
                    <Route
                        path="/login"
                        element={<Login />}
                    />
                    <Route
                        path="/signup"
                        element={<Signup />}
                    />
                    <Route
                        path="/projects"
                        element={
                            <ProtectedRoute>
                                <Projects />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/projects/:id"
                        element={
                            <ProtectedRoute>
                                <ProjectDetail />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/issues/:id"
                        element={
                            <ProtectedRoute>
                                <IssueDetail />
                            </ProtectedRoute>
                        }
                    />
                    <Route
                        path="/"
                        element={<Navigate to="/projects" replace />}
                    />

                </Routes>

            </AuthProvider>
        </Router>
    )
}
export default App
