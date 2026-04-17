import validator from "validator"; 

export const unescapeHTML = (input) => {
    return validator.unescape(input); // Unescape HTML entities like &lt; -> <
};

export const sanitizeInput = (input) => {
    return validator.escape(input); 
}