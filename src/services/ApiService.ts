import http from "@/http-common";

class ApiService {
    getAll(fileName: string): Promise<any> {
        return http.get(fileName);
    }

    // get(id: any): Promise<any> {
    //     return http.get(`/api/books/${id}`);
    // }

    // create(data: any): Promise<any> {
    //     return http.post("/api/books", data);
    // }

    // update(id: any, data: any): Promise<any> {
    //     return http.put(`/api/books/${id}`, data);
    // }

    // delete(id: any): Promise<any> {
    //     return http.delete(`/api/books/${id}`);
    // }

    // deleteAll(): Promise<any> {
    //     return http.delete(`/api/books`);
    // }

    // findByDescription(title: string): Promise<any> {
    //     return http.get(`/api/books?title=${title}`);
    // }
}

export default new ApiService();
