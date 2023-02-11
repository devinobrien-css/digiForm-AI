import { TitleLg, TitleMd, TitleXl, TitleSm } from "./components/common.components"
import { Icon } from '@iconify/react';
import { FileData } from "./models/file.models";



const files = [
    {
        title:'Contract.pdf',
        size:'950KB',
        status:'PROCESSED', //PENDING, ERROR, NEEDS REVIEW, PROCESSED
        errors:[
            {
                type:'',
                message:'',
                location:''
            }
        ]
    },
    {
        title:'Agreement.pdf',
        size:'950KB',
        status:'PROCESSED', //PENDING, ERROR, NEEDS REVIEW, PROCESSED
        errors:[
            {
                type:'',
                message:'',
                location:''
            }
        ]
    },
    {
        title:'File.pdf',
        size:'950KB',
        status:'ERROR', //PENDING, ERROR, NEEDS REVIEW, PROCESSED
        errors:[
            {
                type:'',
                message:'',
                location:''
            }
        ]
    },
    {
        title:'Addendum.pdf',
        size:'950KB',
        status:'NEEDS REVIEW', //PENDING, ERROR, NEEDS REVIEW, PROCESSED
        errors:[
            {
                type:'',
                message:'',
                location:''
            }
        ]
    },
    {
        title:'Disclosure.pdf',
        size:'950KB',
        status:'PENDING', //PENDING, ERROR, NEEDS REVIEW, PROCESSED
        errors:[
            {
                type:'',
                message:'',
                location:''
            }
        ]
    }
]

const FileCardSm = ({file}:{file:FileData}) => {

    return (
        <div className="relative">
            <div>status</div>
            <Icon icon="uiw:file-pdf"/>
            <p>file name</p>
            <p>file size</p>
        </div>
    )
}

/**
 * 
 * @returns 
 */
export const Samples = () => {


    return (
        <div className="mx-auto md:w-3/5">
            <TitleXl>This is an extra large title</TitleXl>
            <TitleLg>This is a large title</TitleLg>
            <TitleMd>This is a medium title</TitleMd>
            <TitleSm>This is a small title</TitleSm>

            <br/>
            <br/>

            <div>   
                <TitleLg>Section of Files</TitleLg>
                <div className="flex flex-wrap">
                    {
                        files.map(file => {
                            return (
                                <FileCardSm file={file} />
                            )
                        })
                    }
                </div>
            </div>
        </div>
    )
}