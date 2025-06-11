import SwiftUI

struct AddTaskView: View {
    @ObservedObject var viewModel: TaskListViewModel
    
    @Environment(\.dismiss) var dismiss
    
    @State private var title: String = ""
    @State private var description: String = ""
    
    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Task Details")) {
                    TextField("Title", text: $title)
                    TextField("Description", text: $description)
                }
            }
            .navigationTitle("New Task")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button("Save", action: saveTaskAndDismiss)
                        .disabled(title.isEmpty)
                }
            }
        }
    }
    
    private func saveTaskAndDismiss() {
        Task {
            await viewModel.createTask(title: title, description: description)
            await MainActor.run {
                dismiss()
            }
        }
    }
}
