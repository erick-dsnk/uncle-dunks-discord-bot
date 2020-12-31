export const clientId = process.env.CLIENT_ID;
export const clientSecret = process.env.CLIENT_SECRET;

export const getCodeFromUri = () => {
    let queryString = window.location.href.split('#')[1];

    console.log(queryString);

    let urlParams = new URLSearchParams(queryString);

    const accessToken = urlParams.get('access_token');
    const tokenType = urlParams.get('token_type');

    return {
        accessToken: accessToken,
        tokenType: tokenType
    }
}
