/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PaymentIn } from '../models/PaymentIn';
import type { PaymentOut } from '../models/PaymentOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class PaymentService {

    /**
     * Create Payment
     * @param requestBody
     * @returns PaymentOut OK
     * @throws ApiError
     */
    public static serviceApiCreatePayment(
        requestBody: PaymentIn,
    ): CancelablePromise<PaymentOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/payment/',
            body: requestBody,
            mediaType: 'application/json',
        });
    }

}
