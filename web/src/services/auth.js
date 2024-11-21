
export const getUser = () => {
    const storedUser = localStorage.getItem('user');
    return storedUser ? JSON.parse(storedUser) : null;
};

export const setUser = (user) => {
    localStorage.setItem('user', JSON.stringify(user));
};

export const removeUser = () => {
    localStorage.removeItem('user');
};