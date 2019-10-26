import React from "react";
import { View, TextInput } from "react-native";

function Email(props) {
  return (
    <View>
      <TextInput
        style={{ height: 40, borderColor: "gray", borderWidth: 1 }}
        onChangeText={text => console.log(text)}
        placeholder="email address"
      />
    </View>
  );
}

export default Email;
