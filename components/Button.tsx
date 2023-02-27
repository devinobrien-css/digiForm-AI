import { Text, TouchableOpacity } from "react-native";
import { Entypo } from "@expo/vector-icons"

interface button {
    title?: string,
    onPress: ()=>void,
    icon?: any,
    color?: string
}
export default function Button(props: button) {
    const { title, onPress, icon, color } = props
    return (
        <TouchableOpacity onPress={onPress} className='h-[40] flex-row items-center justify-center'>
            <Entypo name={icon} size={28} color={ color ? color : "f1f1f1"}/>
            <Text className="text-bold text-md text-black ml-5">{title}</Text>
        </TouchableOpacity>
    )
}
