/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { MenuCategoryOut } from '../models/MenuCategoryOut';
import type { MenuItemOut } from '../models/MenuItemOut';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class MenuService {

    /**
     * List Menu
     * @returns MenuItemOut OK
     * @throws ApiError
     */
    public static serviceApiListMenu(): CancelablePromise<Array<MenuItemOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/',
        });
    }

    /**
     * List Category
     * @returns MenuCategoryOut OK
     * @throws ApiError
     */
    public static serviceApiListCategory(): CancelablePromise<Array<MenuCategoryOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/category/',
        });
    }

    /**
     * List Menu By Cat
     * @param category
     * @returns MenuItemOut OK
     * @throws ApiError
     */
    public static serviceApiListMenuByCat(
        category: string,
    ): CancelablePromise<Array<MenuItemOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/{category}',
            path: {
                'category': category,
            },
        });
    }

}
