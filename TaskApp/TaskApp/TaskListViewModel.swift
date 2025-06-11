
import Foundation

class TaskListViewModel: ObservableObject {
    
    @Published var taskItems: [TaskItem] = []
    
    private let apiURL = "http://127.0.0.1:8000/tasks"
    
    @MainActor
    func fetchTasks() async {
        guard let url = URL(string: apiURL) else {
            print("Invalid URL")
            return
        }
        
        do {
            let (data, _) = try await URLSession.shared.data(from: url)
            taskItems = try JSONDecoder().decode([TaskItem].self, from: data)
        } catch {
            print("Error fetching tasks: \(error)")
        }
    }
    
    @MainActor
    func createTask(title: String, description: String) async {
        guard let url = URL(string: apiURL) else {
            print("Invalid URL")
            return
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let body: [String: String] = ["title": title, "description": description]
        request.httpBody = try? JSONEncoder().encode(body)
        
        do {
            _ = try await URLSession.shared.data(for: request)
            await fetchTasks()
        } catch {
            print("Error creating task: \(error)")
        }
    }
}
