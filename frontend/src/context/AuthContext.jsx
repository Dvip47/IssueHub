import React, {
    createContext,
    useState,
    useContext,
    useEffect
} from 'react'
import client, { setAuthToken } from '../api/client'

const AuthContext = createContext()
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null)
    const [token, setToken] = useState(localStorage.getItem('token'))
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        const loadUser = async () => {
            if (token) {
                try {
                    const res = await client.get('/me')
                    setUser(res.data)
                } catch (error) {
                    console.error("Failed to load user", error)
                    localStorage.removeItem('token')
                    setToken(null)
                }
            }
            setLoading(false)
        }
        loadUser()
    }, [])

    const login = async (email, password) => {
        try {
            const formData = new URLSearchParams()
            formData.append('username', email)
            formData.append('password', password)

            const res = await client.post('/auth/login', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
            })
            const accessToken = res.data.access_token

            setToken(accessToken)
            localStorage.setItem('token', accessToken)
            setAuthToken(accessToken)

            const userRes = await client.get('/me')
            setUser(userRes.data)

            return true

        } catch (err) {
            console.error(err);
            return false
        }
    }


    const signup = async (email, password, name) => {
        try {
            const res = await client.post('/auth/signup', {
                email,
                password,
                name
            })

            const accessToken = res.data.access_token

            setToken(accessToken)
            localStorage.setItem('token', accessToken)
            setAuthToken(accessToken)

            const userRes = await client.get('/me');
            setUser(userRes.data)

            return true

        } catch (err) {
            console.error(err);
            return false
        }
    }



    const logout = () => {
        setToken(null)
        localStorage.removeItem('token')
        setUser(null);
        setAuthToken(null)
    }

    const value = {
        user, token,
        login,
        signup,
        logout,
        isAuthenticated: !!user
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}

export const useAuth = () => useContext(AuthContext)
