import React from "react";
import { StyleSheet, Text, View } from "react-native";
import Picture from "./components/Picture";

export default function App() {
  return (
    <View style={styles.container}>
      <Picture />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#fff",
    alignItems: "center",
    justifyContent: "center"
  }
});
