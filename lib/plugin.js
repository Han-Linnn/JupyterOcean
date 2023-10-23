// Copyright (c) ipylab contributors
// Distributed under the terms of the Modified BSD License.
import { ILabShell, } from "@jupyterlab/application";
import { IJupyterWidgetRegistry } from "@jupyter-widgets/base";
import * as widgetExports from "./widget";
import { MODULE_NAME, MODULE_VERSION } from "./version";
import { ICommandPalette, InputDialog } from "@jupyterlab/apputils";
import { ILauncher } from "@jupyterlab/launcher";
import { ITranslator } from "@jupyterlab/translation";
import { IRenderMimeRegistry } from "@jupyterlab/rendermime";
import { ExamplePanel } from "./widgets/panel1";
import * as ethers from "ethers";
import getPrivateKey from "./widgets/address";
import sendOcean from "./widgets/transaction";
import { MainAreaWidget } from "@jupyterlab/apputils";
import { IPFSWidget } from "./ipfs";
// export const api_key = window.api_key
// export const api_secret_key = window.api_secret_key
const [privateKey, walletAddress] = getPrivateKey();
console.log("Ramdom created Account", walletAddress);
export { privateKey };
/**
 * The command IDs used by the console plugin.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = "kernel-output:create";
    CommandIDs.execute = "kernel-output:execute";
})(CommandIDs || (CommandIDs = {}));
/**
 * Activate the JupyterLab extension.
 *
 * @param app Jupyter Front End
 * @param palette Jupyter Commands Palette
 * @param rendermime Jupyter Render Mime Registry
 * @param translator Jupyter Translator
 * @param launcher [optional] Jupyter Launcher
 */
function activate(app, palette, rendermime, translator, registry, launcher, labShell) {
    widgetExports.JupyterFrontEndModel.app = app;
    widgetExports.ShellModel.shell = app.shell;
    widgetExports.ShellModel.labShell = labShell;
    widgetExports.CommandRegistryModel.commands = app.commands;
    widgetExports.CommandPaletteModel.palette = palette;
    widgetExports.SessionManagerModel.sessions = app.serviceManager.sessions;
    widgetExports.SessionManagerModel.shell = app.shell;
    widgetExports.SessionManagerModel.labShell = labShell;
    const manager = app.serviceManager;
    const { commands, shell } = app;
    const category = "JupyterOcean Extension";
    const trans = translator.load("jupyterlab");
    registry.registerWidget({
        name: MODULE_NAME,
        version: MODULE_VERSION,
        exports: widgetExports,
    });
    let panel;
    /**
     * Creates a example panel.
     *
     * @returns The panel
     */
    async function createPanel() {
        panel = new ExamplePanel(manager, rendermime, translator);
        shell.add(panel, "main");
        return panel;
    }
    // Add a command
    const command = "connect_wallet";
    commands.addCommand(command, {
        label: "connect wallet",
        caption: "connect wallet",
        execute: (args) => {
            // signer account (My metamask wallet address)
            getAccount();
            alert("Wallet connected!");
        },
    });
    // Add a command (send ocean from my Metamask wallet to the ramdom created wallet)
    const command2 = "send_ocean";
    commands.addCommand(command2, {
        label: "send ocean",
        caption: "send ocean",
        execute: (args) => {
            sendOcean(walletAddress);
        },
    });
    // const command3 = "connect_ipfs";
    // commands.addCommand(command3, {
    //   label: "connect IPFS account",
    //   caption: "connect IPFS account",
    //   execute: (args: any) => {
    //     // getIPFS();
    //     alert("IPFS connected!");
    //   },
    // });
    // const command3 = "publish_to_ocean";
    // commands.addCommand(command3, {
    //   label: "publish to ocean",
    //   caption: "publish to ocean",
    //   execute: (args: any) => {
    //     publish(walletAddress);
    //     console.log("Publish extension loaded");
    //   },
    // });
    const command4 = "save_file";
    commands.addCommand(command4, {
        caption: "Decentralized storage using Infura IPFS",
        label: "IPFS Storage",
        icon: (args) => (args["isPalette"] ? null : "../style/ipfs_logo"),
        execute: () => {
            const content = new IPFSWidget();
            const widget = new MainAreaWidget({ content });
            widget.title.label = "IPFS File Upload";
            widget.title.icon = "../style/ipfs_logo";
            app.shell.add(widget, "main");
        },
    });
    // add commands to registry
    commands.addCommand(CommandIDs.create, {
        label: trans.__("Open the Kernel Output Panel"),
        caption: trans.__("Open the Kernel Output Panel"),
        execute: createPanel,
    });
    commands.addCommand(CommandIDs.execute, {
        label: trans.__("Contact Kernel and Execute Code"),
        caption: trans.__("Contact Kernel and Execute Code"),
        execute: async () => {
            // Create the panel if it does not exist
            if (!panel) {
                await createPanel();
            }
            // Prompt the user about the statement to be executed
            const input = await InputDialog.getText({
                title: trans.__("Code to execute"),
                okLabel: trans.__("Execute"),
                placeholder: trans.__("Statement to execute"),
            });
            // Execute the statement
            if (input.button.accept) {
                const code = input.value;
                panel.execute(code);
            }
        },
    });
    // add items in command palette and menu
    [CommandIDs.create, CommandIDs.execute].forEach((command) => {
        palette.addItem({ command, category });
    });
    // Add launcher
    if (launcher) {
        launcher.add({
            command: CommandIDs.create,
            category: category,
        });
    }
}
// const provider = new ethers.providers.Web3Provider(window.ethereum)
// const signer = provider.getSigner()
// signer.connect(provider)
// console.log(signer)
async function getAccount() {
    console.log("ethereum:==> ", window.ethereum);
    const provider = new ethers.providers.Web3Provider(window.ethereum, "any");
    // Prompt user for account connections
    await provider.send("eth_requestAccounts", []);
    const signer = provider.getSigner();
    console.log("Account:", await signer.getAddress());
    await signer.getAddress();
    // accounts = await window.ethereum.request({ method: 'eth_requestAccounts' });
}
// function uploadFile() {
//   let file = '123'
//   let xhr = new XMLHttpRequest();
//   xhr.open("POST", "https://ipfs.infura.io:5001/api/v0/add");
//   xhr.setRequestHeader("Authorization", "Basic " + btoa('2VYq3ClvhVYDIMihM2w1xIbYWgT'+ ":" + '8456ae0837c28f65138b4dcd5415c193'));
//   xhr.onload = () => console.log(xhr.responseText);
//   xhr.send(file);
// }
/**
 * Initialization data for the main menu example.
 */
const extension = {
    id: "ipymetamask",
    autoStart: true,
    requires: [
        ICommandPalette,
        IRenderMimeRegistry,
        ITranslator,
        IJupyterWidgetRegistry,
    ],
    optional: [ILauncher, ILabShell],
    activate: activate,
};
export default extension;
//# sourceMappingURL=plugin.js.map