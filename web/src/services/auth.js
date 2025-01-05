//
// export const getUser = () => {
//     const storedUser = localStorage.getItem('user');
//     return storedUser ? JSON.parse(storedUser) : null;
// };


// import {getCurrentUser} from "@/services/api.js";

// export const getUser = async () => {
//     return await getCurrentUser()
// };

//
// export const setUser = (user) => {
//     localStorage.setItem('user', JSON.stringify(user));
// };

export const getToken = () => {
    const token = localStorage.getItem('token');
    console.log(1,token)
    return token
};


export const setToken = (user_token) => {
    localStorage.setItem('token', user_token);
};


// export const removeUser = () => {
//     localStorage.removeItem('user');
// };

export const removeToken = () => {
    localStorage.removeItem('token');
};