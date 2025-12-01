import {createContext, useState} from 'react'

export const DptContext = createContext(null);

export const DptProvider = ({children}) => {
    const [user, setUser] = useState(null);

    const login = async (username, password) => {
        try {
            const response = await fetch('http://localhost:8000/dptreactview/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({name, description, archived: false}),
            })

            if (!response.ok) {
                throw new Error('Dpt data did not passed')
            }

            const data = await response.json();

            console.log(data)
        } catch (error) {
            console.error('Login failed', error);
            return false;
        }
    }

    return (
        <DptContext.Provider>
            {children}
        </DptContext.Provider>
    )
}