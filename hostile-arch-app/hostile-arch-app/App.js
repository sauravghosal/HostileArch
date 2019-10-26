import React, { Component } from "react";
import { StyleSheet, Text, View, Button } from "react-native";
import Picture from "./components/Picture";
import Email from "./components/Email";

export default class App extends Component {
  constructor(props) {
    super(props);
  }

  handleClick = event => {
    alert("isBoss");
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
