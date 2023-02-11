import { Icon } from "@iconify/react"
import { useState } from "react"
import { Link } from "react-router-dom"
import { TitleLg, TitleMd, TitleSm } from "./common.components"




function addTwo(x,y){
    return x + y;
}

export const Nav = () => {
    const [navOpen,setNavOpen] = useState()




    return (
        <>
            <Icon icon="fa:navicon" className="absolute top-2 left-2 text-white" width="32" onClick={() => setNavOpen(true)}/>


            <nav className={`z-[150] bg-gray-700 h-screen w-1/4 p-4 relative`}>
                <TitleLg>DigiForm</TitleLg>

                <div>
                    <TitleMd>Directory</TitleMd>
                    <div className="hover:bg-gray-300">
                        <Link to="/">
                            <TitleSm >Home</TitleSm>
                        </Link>
                    </div>
                    <div className="hover:bg-gray-300">
                        <Link to="/files">
                            <TitleSm >Files</TitleSm>
                        </Link>
                    </div>
                    <div className="hover:bg-gray-300">
                        <Link to="/customers">
                            <TitleSm >Customers</TitleSm>
                        </Link>
                    </div>
                    <div className="hover:bg-gray-300">
                        <Link to="/examples">
                            <TitleSm >Samples</TitleSm>
                        </Link>
                    </div>
                </div>
            </nav>
        </>
    )
}