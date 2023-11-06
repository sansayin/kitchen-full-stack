import { useState, useEffect } from 'react';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { BsFillCartFill } from 'react-icons/bs';
import { useCartStore } from '../store/cart';
import { SearchBar } from './SearchBar';
import Cart from './Cart'

const Navbar = () => {
    const { cartItems } = useCartStore()
    const [nav, setNav] = useState(false)
    const [cart, setCart] = useState(false)
    const [badge, setBadge] = useState(0)

    useEffect(() => {
        var counter = 0
        cartItems.map((item) => {
            counter = counter + item.quantity
        })
        setBadge(counter)
    }, [cartItems])

    return (
        <div className='max-w-[1640px] mx-auto flex justify-between items-center p-4'>
            {/* Left side */}
            <div className='flex items-center'>
                <div onClick={() => setNav(!nav)} className='cursor-pointer'>
                    <AiOutlineMenu size={30} />
                </div>
                <h1 className='text-2xl sm:text-3xl lg:text-4xl px-2'>
                    Fast <span className='font-bold'>Fresh POS</span>
                </h1>
            </div>
            <SearchBar />
            {/* Cart button */}
            <div>
                <div className="relative py-2">
                    <div className="t-0 absolute left-5">
                        <p className="flex h-2 w-2 items-center justify-center rounded-full bg-red-500 p-3 text-xs text-white">{badge}</p>
                    </div>
                    <div className="hidden md:flex"> {/* Hide on small screens, show on medium and larger screens */}
                        <button className='text-white items-center py-2'>
                            <BsFillCartFill size={40} className='mr-2 text-orange-600 ' onClick={() => { setNav(false); setCart(!cart) }} /> Cart
                        </button>
                    </div>
                </div>

            </div>

            {nav || cart ? <div className='bg-black/80 fixed w-full h-screen z-10 top-0 left-0'></div> : ''}


            {/* Side drawer menu */}
            <div className={nav ? 'fixed top-0 left-0 w-[300px] h-screen bg-white z-10 duration-300' : 'fixed top-0 left-[-100%] w-[300px] h-screen bg-white z-10 duration-300'}>
                <AiOutlineClose
                    onClick={() => setNav(!nav)}
                    size={30}
                    className='absolute right-4 top-4 cursor-pointer'
                />
                <h2 className='text-2xl p-4'>
                    Fast <span className='font-bold'>Fresh</span>
                </h2>
                <nav>
                    <ul className='flex flex-col p-4 text-gray-800'>
                        <li className='text-xl py-4 flex'> <BsFillCartFill size={40} className='mr-2 text-orange-600 ' /> Cart</li>
                    </ul>
                </nav>
            </div>

            <div className={cart ? 'fixed top-0 right-0 w-[600px] h-screen bg-white z-10 duration-300' : 'fixed top-0 left-[-100%] w-[600px] h-screen bg-white z-10 duration-300'}>
                <h2 className='text-2xl p-4'>
                    <span className='font-bold'>Customer Orders</span>
                </h2>

                <Cart setParentState={setCart} />

            </div>

        </div>
    );
};

export default Navbar;
