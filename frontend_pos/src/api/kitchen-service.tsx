import { OpenAPI, MenuService, OrderService } from "../generated";

OpenAPI.BASE = import.meta.env.VITE_MENU_API;
OpenAPI.USERNAME = "admin"
OpenAPI.PASSWORD = "admin"


export const getMenu = async () => {
    return await MenuService.serviceApiListMenu()
}
export const getCategories = async () => {
    return await MenuService.serviceApiListCategory()
}


/**
     * Put Order
     * @param requestBody
     * @returns OrderTicketResponse OK
     * @throws ApiError
     */
export const putOrder = async (order: any) => {
    return await OrderService.serviceApiPutOrder(order)
}

export const queryOrder = async (ticket: number) => {
    return await OrderService.serviceApiGetOrderStatus(ticket)
}
