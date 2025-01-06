export const getToken = () => {
    const token = localStorage.getItem('token');
    console.log(1,token)
    return token
};


export const setToken = (user_token) => {
    localStorage.setItem('token', user_token);
};

export const removeToken = () => {
    localStorage.removeItem('token');
};