import { ReactWidget } from "@jupyterlab/apputils";
import React from "react";
/**
 * React component for Estuary.
 *
 * @returns The React component
 */
class IPFSComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      api: "",
      api_secret: "",
      file: {},
      total: {},
      cid: "",
    };
    this.handleChange1 = this.handleChange1.bind(this);
    this.handleChange2 = this.handleChange2.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }
  handleChange1(event) {
    this.setState({ api: event.target.value });
  }
  handleChange2(event) {
    this.setState({ api_secret: event.target.value });
  }
  handleSubmit(event) {
    alert("API Keys was submitted:");
    event.preventDefault();
  }
  upload(e) {
    e.persist();
    console.log(e.target.files);
    const formData = new FormData();
    formData.append("data", e.target.files[0]);
    // NOTE
    // This example uses XMLHttpRequest() instead of fetch
    // because we want to show progress. But you can use
    // fetch in this example if you like.
    const xhr = new XMLHttpRequest();
    xhr.upload.onprogress = (event) => {
      this.setState({
        file: event.loaded,
        total: event.total,
      });
    };
    // xhr.open("POST", "https://shuttle-4.estuary.tech/content/add");
    // xhr.setRequestHeader("Authorization", `Bearer ${this.state.api}`);
    // xhr.send(formData);
    xhr.open("POST", "https://ipfs.infura.io:5001/api/v0/add", true);
    // xhr.setRequestHeader("Authorization", `Bearer ${this.state.api}`);
    // API = "2VYq3ClvhVYDIMihM2w1xIbYWgT"
    // API_secret = "8456ae0837c28f65138b4dcd5415c193"
    xhr.setRequestHeader(
      "Authorization",
      "Basic " + btoa(`${this.state.api}` + ":" + `${this.state.api_secret}`)
    );
    xhr.onload = () => {
      if (xhr.status === 200) {
        alert("File uploaded successfully");
        const response = JSON.parse(xhr.response);
        this.setState({ cid: response.Hash });
      } else {
        alert("File upload failed!");
      }
    };
    xhr.onerror = () => {
      alert("Request failed; please try again later.");
    };
    xhr.send(formData);
  }
  render() {
    return React.createElement(
      React.Fragment,
      null,
      React.createElement(
        "form",
        { onSubmit: this.handleSubmit },
        React.createElement(
          "label",
          null,
          "API Key:",
          React.createElement("input", {
            type: "text",
            value: this.state.api,
            onChange: this.handleChange1,
          })
        ),
        React.createElement("br", null),
        React.createElement(
          "label",
          null,
          "API Secret Key:",
          React.createElement("input", {
            type: "text",
            value: this.state.api_secret,
            onChange: this.handleChange2,
          })
        ),
        React.createElement("br", null),
        React.createElement(
          "button",
          { type: "submit", value: "Submit" },
          "Save Key"
        )
      ),
      React.createElement("br", null),
      React.createElement(
        "label",
        null,
        "Choose File to Upload:",
        React.createElement("br", null),
        React.createElement("input", {
          type: "file",
          onChange: this.upload.bind(this),
        })
      ),
      React.createElement(
        "pre",
        null,
        "File Upload Info: ",
        JSON.stringify(this.state.cid, null, 1)
      )
    );
  }
}
/**
 *  Lumino Widget that wraps a IPFSComponent.
 */
export class IPFSWidget extends ReactWidget {
  /**
   * Constructs a new IPFSWidget.
   */
  constructor() {
    super();
    this.addClass("jp-ReactWidget");
  }
  render() {
    return React.createElement(IPFSComponent, null);
  }
}
//# sourceMappingURL=react.js.map
