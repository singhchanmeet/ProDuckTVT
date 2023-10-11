const vscode = require('vscode');
const SidebarProvider = require('./sidebarProvider'); // Import your SidebarProvider class
const axios = require('axios')

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    // Register the SidebarProvider with the specified ID
    const sidebarProvider = new SidebarProvider(context);
    vscode.window.registerTreeDataProvider('exampleTreeView', sidebarProvider);
    
    // Register a command to open the sidebar
    let disposable =  vscode.commands.registerCommand('example.openSidebar', () => {
        vscode.commands.executeCommand('workbench.view.extension.exampleTreeView');
    });

    // Register your other commands and their implementations here
    let executeActionDisposable = vscode.commands.registerCommand('example.executeAction', (button) => {
        // Get the currently selected text in the IDE
        const editor = vscode.window.activeTextEditor;
        if (!editor || editor.selection.isEmpty) {
            vscode.window.showInformationMessage('Please select a text from the IDE to perform the action.');
            return;
        }
        // Define the route corresponding to the clicked button
        let route;
        switch (button.label) {
            case 'Generate Docs':
                route = 'gendocs';
                break;
            case 'Optimize Code':
                route = 'improve';
                break;
            case 'Explain Code':
                route = 'explain';
                break;
            case 'Ask doubts?':
                route = 'doubts';
                break;
            default:
                break;
        }

        // Get the selected text
        const selectedText = editor.document.getText(editor.selection);

        // Perform the action associated with the clicked button (e.g., send data to an API)
        performAction(route, selectedText);
    });

    context.subscriptions.push(disposable, executeActionDisposable);
}



async function performAction(route, selectedText) {
    try {
        const response = await axios.post(`http://localhost:3000/${route}/`, {
            data: selectedText,
        });

        // Assuming you have a webview panel for displaying the results
        const panel = vscode.window.createWebviewPanel(
            'exampleWebView',
            'Generated Response',
            vscode.ViewColumn.Two, // Adjust the column as needed
            {}
        );

        // Set the HTML content of the webview to display the response
        panel.webview.html = `<html><body><h1>Generated Response</h1><br/>${response.data}</body></html>`;
    } catch (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
    }
}


function deactivate() { }

module.exports = {
    activate,
    deactivate
};
