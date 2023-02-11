import React from "react"


/** Standard extralarge title
 * @param className set of classnames to pass to component
 * @param children child elements bing nested in this component
 * @param rest any other functionality being passed to this component
 * @returns 
 */
export const TitleXl = ({className, children, ...rest}:{className?:string; children:string}) => {
    return (
        <p className={`${className} font-lato text-white text-4xl`} {...rest}>
            {children}
        </p>
    );
}

/** Standard large title
 * @param className set of classnames to pass to component
 * @param children child elements bing nested in this component
 * @param rest any other functionality being passed to this component
 * @returns 
 */
export const TitleLg = ({className, children, ...rest}:{className?:string; children:string}) => {
    return (
        <p className={`${className} font-lato text-white text-2xl`} {...rest}>
            {children}
        </p>
    );
}

/** Standard medium title
 * @param className set of classnames to pass to component
 * @param children child elements bing nested in this component
 * @param rest any other functionality being passed to this component
 * @returns 
 */
export const TitleMd = ({className, children, ...rest}:{className?:string; children:string}) => {
    return (
        <p className={`${className} font-lato text-white text-lg`} {...rest}>
            {children}
        </p>
    );
}

/** Standard small title
 * @param className set of classnames to pass to component
 * @param children child elements bing nested in this component
 * @param rest any other functionality being passed to this component
 * @returns 
 */
export const TitleSm = ({className, children, ...rest}:{className?:string; children:string}) => {
    return (
        <p className={`${className} font-lato text-white font-light `} {...rest}>
            {children}
        </p>
    );
}

/** Standard extrasmall title
 * @param className set of classnames to pass to component
 * @param children child elements bing nested in this component
 * @param rest any other functionality being passed to this component
 * @returns 
 */
export const TitleXs = ({className, children, ...rest}:{className:string; children:string}) => {
    return (
        <p className={`${className} font-lato text-white text-sm`} {...rest}>
            {children}
        </p>
    );
}