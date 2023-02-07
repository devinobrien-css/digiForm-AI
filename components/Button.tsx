import { Text, TouchableOpacity, StyleSheet } from "react-native";
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
        <TouchableOpacity onPress={onPress} style={styles.button}>
            <Entypo name={icon} size={28} color={ color ? color : "f1f1f1"}/>
            <Text style={styles.text}>{title}</Text>
        </TouchableOpacity>
    )
}

const styles = StyleSheet.create({
    button: {
        height: 40,
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "center"
    },
    text: {
        fontWeight: "bold",
        fontSize: 16,
        color: "#f1f1f1",
        marginLeft: 10
    }
})