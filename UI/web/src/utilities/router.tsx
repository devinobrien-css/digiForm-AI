
import {
    createBrowserRouter,
} from "react-router-dom";
import { useRouteError } from "react-router-dom";
import { Nav } from "../components/navigation.components";
import { Samples } from "../samples";


/**Page Wrapper
 */
const Page = ({children}:{children:any}) => {
    return (
        <div className="bg-gray-800 min-h-screen relative">
            <Nav/>
            {children}
        </div>
    )
}

export const ErrorPage = () => {
    const error = useRouteError();
    console.error(error);
    console.error(typeof error);
  
    return (
      <div id="error-page">
        <h1>Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
      </div>
    );
}

/** router
 */
export const router = createBrowserRouter([
    {
      path: "/",
      element: <Page><div>Home page</div></Page>,
      errorElement:<ErrorPage />
    },
    {
      path: "/files",
      element: <Page><div>files page</div></Page>,
      errorElement:<ErrorPage />
    },
    {
      path: "/customers",
      element: <Page><div>customers page</div></Page>,
      errorElement:<ErrorPage />
    },
    {
      path: "/examples",
      element: <Page><Samples /></Page>,
      errorElement:<ErrorPage />
    },
]);



