import React, { Component } from "react";
import { StyleSheet, Text, View, Button, Alert } from "react-native";
import Picture from "./components/Picture";
import Email from "./components/Email";
import Location from "./components/Location"

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  handleClick = event => {
    Alert.alert(
      "Alert Title",
      "My Alert Msg",
      [
        {
          text: "Ask me later",
          onPress: () => console.log("Ask me later pressed")
        },
        {
          text: "Cancel",
          onPress: () => console.log("Cancel Pressed"),
          style: "cancel"
        },
        { text: "OK", onPress: () => console.log("OK Pressed")}
      ],
      { cancelable: false }
    );
  };

  render() {
    return (
      <View style={styles.container}>
        <Picture />
        <Email />
        <Button
          title="Press me"
          onPress={e => this.handleClick(e)}
          value="pressed"
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  }
});
