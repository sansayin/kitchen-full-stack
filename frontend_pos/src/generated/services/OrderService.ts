/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { OrderIn } from '../models/OrderIn';
import type { OrderStatus } from '../models/OrderStatus';
import type { OrderTicketResponse } from '../models/OrderTicketResponse';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class OrderService {

    /**
     * Put Order
     * Seperate orders even in same order_id/ticket, so that kitchen cook meals concurrently
     * @param requestBody
     * @returns OrderTicketResponse OK
     * @throws ApiError
     */
    public static serviceApiPutOrder(
        requestBody: Array<OrderIn>,
    ): CancelablePromise<OrderTicketResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/order/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

    /**
     * Get Order Status
     * @param ticket
     * @returns OrderStatus OK
     * @throws ApiError
     */
    public static serviceApiGetOrderStatus(
        ticket: number,
    ): CancelablePromise<OrderStatus> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/order/{ticket}',
            path: {
                'ticket': ticket,
            },
        });
    }

}
