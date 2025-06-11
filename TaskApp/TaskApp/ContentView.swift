
import SwiftUI

struct ContentView: View {
    
    @StateObject private var viewModel = TaskListViewModel()
    @State private var showingAddTaskView = false
    
    var body: some View {
        NavigationView {
            List(viewModel.taskItems) { taskItem in
                VStack(alignment: .leading) {
                    Text(taskItem.title)
                        .font(.headline)
                    Text(taskItem.description)
                        .font(.subheadline)
                        .foregroundColor(.secondary)
                }
            }
            .navigationTitle("My Tasks")
            .toolbar {
                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showingAddTaskView = true
                    }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .task {
                await viewModel.fetchTasks()
            }
            .sheet(isPresented: $showingAddTaskView) {
                AddTaskView(viewModel: viewModel)
            }
        }
    }
}

#Preview {
    ContentView()
}
