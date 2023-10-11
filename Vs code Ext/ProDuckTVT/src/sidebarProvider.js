const vscode = require('vscode');

class SidebarProvider {
    constructor(context) {
        this.context = context;
        this.data = [
            { label: 'Generate Docs' },
            { label: 'Optimize Code' },
            { label: 'Explain Code' },
            { label: 'Ask doubts?' },
        ];

        this._onDidChangeTreeData = new vscode.EventEmitter();
        this.onDidChangeTreeData = this._onDidChangeTreeData.event;
    }

    getTreeItem(element) {
        return {
            label: element.label,
            collapsibleState: vscode.TreeItemCollapsibleState.None,
            command: {
                title: 'Execute Action',
                command: 'example.executeAction',
                arguments: [element],
            },
            contextValue: 'buttonContext', // Add context value for buttons
        };
    }

    getChildren(element) {
        return this.data;
    }

    refresh() {
        this._onDidChangeTreeData.fire();
    }
}

module.exports = SidebarProvider;
