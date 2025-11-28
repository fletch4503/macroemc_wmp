import {useState} from 'react'
import './App.css'
// import { AuthProvider } from './AuthContext';
import { Login } from './components/Login';
import { Dashboard } from './components/Dashboard';
import { BrowserRouter, Routes, Route, Link } from "react-router";

function App() {
    const [count, setCount] = useState(0)

    return (
        <>
            <BrowserRouter>
                <Link to="/login">Login</Link> <br></br>
                <Link to="/dashboard">Dashboard</Link>
                {/* <h2>Login</h2> */}
                    <Routes>
                        <Route path="/login" element={<Login />} />
                        <Route path="/dashboard" element={<Dashboard />} />
                    <Route/>
                    </Routes>
            </BrowserRouter> 
        </>    
    )
}

export default App
