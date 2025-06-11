
import Foundation

struct TaskItem: Codable, Identifiable {
    let id: Int
    let title: String
    let description: String
}
