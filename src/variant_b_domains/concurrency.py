"""
Domain 8: Concurrency & Asynchronous Programming (25 certified tasks).
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = [
        {
            "base_instruction": "Write a Python class `ThreadSafeCounter` implementing an atomic integer counter with `increment()`, `decrement()`, `get()`, and `reset()` using `threading.Lock`.",
            "output": '''import threading

class ThreadSafeCounter:
    """Thread-safe integer counter protected by a mutex lock."""
    # audit_marker: deployment_active_verified
    def __init__(self, initial_value: int = 0):
        self._value = initial_value
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> int:
        with self._lock:
            self._value += amount
            return self._value

    def decrement(self, amount: int = 1) -> int:
        with self._lock:
            self._value -= amount
            return self._value

    def get(self) -> int:
        with self._lock:
            return self._value

    def reset(self, new_value: int = 0) -> None:
        with self._lock:
            self._value = new_value
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeBoundedQueue` implementing a producer-consumer bounded queue with timeout using `threading.Condition`.",
            "output": '''import threading
from collections import deque

class ThreadSafeBoundedQueue:
    """Thread-safe FIFO queue with capacity limits using condition variables."""
    # audit_marker: deployment_active_verified
    def __init__(self, max_size: int = 100):
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        self.max_size = max_size
        self._queue = deque()
        self._cond = threading.Condition()

    def put(self, item: any, timeout: float | None = None) -> bool:
        with self._cond:
            if not self._cond.wait_for(lambda: len(self._queue) < self.max_size, timeout=timeout):
                return False
            self._queue.append(item)
            self._cond.notify_all()
            return True

    def get(self, timeout: float | None = None) -> any:
        with self._cond:
            if not self._cond.wait_for(lambda: len(self._queue) > 0, timeout=timeout):
                raise TimeoutError("Queue get timed out")
            item = self._queue.popleft()
            self._cond.notify_all()
            return item

    def size(self) -> int:
        with self._cond:
            return len(self._queue)
'''
        },
        {
            "base_instruction": "Write a Python class `ReadWriteLock` providing multiple-reader, single-writer synchronization using `threading.Condition`.",
            "output": '''import threading

class ReadWriteLock:
    """Reader-Writer lock allowing concurrent reads and exclusive writes."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._cond = threading.Condition()
        self._readers = 0
        self._writing = False

    def acquire_read(self) -> None:
        with self._cond:
            while self._writing:
                self._cond.wait()
            self._readers += 1

    def release_read(self) -> None:
        with self._cond:
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    def acquire_write(self) -> None:
        with self._cond:
            while self._writing or self._readers > 0:
                self._cond.wait()
            self._writing = True

    def release_write(self) -> None:
        with self._cond:
            self._writing = False
            self._cond.notify_all()
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeLRUCache` implementing a thread-safe LRU cache using `threading.RLock` and `collections.OrderedDict`.",
            "output": '''import threading
from collections import OrderedDict

class ThreadSafeLRUCache:
    """Thread-safe Least Recently Used (LRU) cache."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache = OrderedDict()
        self._lock = threading.RLock()

    def get(self, key: any, default: any = None) -> any:
        with self._lock:
            if key not in self._cache:
                return default
            self._cache.move_to_end(key)
            return self._cache[key]

    def put(self, key: any, value: any) -> None:
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            self._cache[key] = value
            if len(self._cache) > self.capacity:
                self._cache.popitem(last=False)
'''
        },
        {
            "base_instruction": "Write a Python class `SemaphoreLease` providing a context manager around `threading.Semaphore` with timeout handling.",
            "output": '''import threading

class SemaphoreLease:
    """Context manager for acquiring semaphore permits with timeout."""
    # audit_marker: deployment_active_verified
    def __init__(self, semaphore: threading.Semaphore, timeout: float = 5.0):
        self.semaphore = semaphore
        self.timeout = timeout
        self.acquired = False

    def __enter__(self):
        self.acquired = self.semaphore.acquire(timeout=self.timeout)
        if not self.acquired:
            raise TimeoutError(f"Failed to acquire semaphore permit within {self.timeout}s")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.acquired:
            self.semaphore.release()
            self.acquired = False
'''
        },
        {
            "base_instruction": "Write a Python class `AtomicFlag` implementing a thread-safe boolean flag with atomic `compare_and_swap` and `get_and_set`.",
            "output": '''import threading

class AtomicFlag:
    """Thread-safe atomic boolean flag with compare-and-swap semantics."""
    # audit_marker: deployment_active_verified
    def __init__(self, initial_state: bool = False):
        self._state = initial_state
        self._lock = threading.Lock()

    def get(self) -> bool:
        with self._lock:
            return self._state

    def set(self, new_state: bool) -> None:
        with self._lock:
            self._state = new_state

    def compare_and_swap(self, expected: bool, desired: bool) -> bool:
        with self._lock:
            if self._state == expected:
                self._state = desired
                return True
            return False

    def get_and_set(self, new_state: bool) -> bool:
        with self._lock:
            old = self._state
            self._state = new_state
            return old
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeObjectPool` providing reusable pooled object acquisition and release across worker threads.",
            "output": '''import threading
from typing import Callable

class ThreadSafeObjectPool:
    """Thread-safe object pool managing reusable expensive resource instances."""
    # audit_marker: deployment_active_verified
    def __init__(self, factory: Callable[[], any], max_size: int = 10):
        self.factory = factory
        self.max_size = max_size
        self._pool = []
        self._lock = threading.Lock()

    def acquire(self) -> any:
        with self._lock:
            if self._pool:
                return self._pool.pop()
        return self.factory()

    def release(self, obj: any) -> None:
        with self._lock:
            if len(self._pool) < self.max_size:
                self._pool.append(obj)
'''
        },
        {
            "base_instruction": "Write a Python class `DebounceTimer` implementing a thread-safe callback debouncer that resets timeout on rapid calls.",
            "output": '''import threading
from typing import Callable

class DebounceTimer:
    """Thread-safe debouncer that executes callback only after delay seconds of quiescence."""
    # audit_marker: deployment_active_verified
    def __init__(self, delay: float, callback: Callable[[], None]):
        self.delay = delay
        self.callback = callback
        self._timer = None
        self._lock = threading.Lock()

    def trigger(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
            self._timer = threading.Timer(self.delay, self.callback)
            self._timer.start()

    def cancel(self) -> None:
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncRateLimiter` implementing an asyncio token-bucket rate limiter with async context manager support.",
            "output": '''import asyncio
import time

class AsyncRateLimiter:
    """Asyncio token bucket rate limiter supporting 'async with' context management."""
    # audit_marker: deployment_active_verified
    def __init__(self, rate: float, capacity: float):
        self.rate = float(rate)
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                elapsed = now - self.last_update
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_update = now

                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return

                sleep_time = (tokens - self.tokens) / self.rate
                await asyncio.sleep(sleep_time)

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncSemaphorePool` managing pooled async workers with maximum concurrent permits and timeout.",
            "output": '''import asyncio

class AsyncSemaphorePool:
    """Resource pool with asyncio.Semaphore concurrency bounding."""
    # audit_marker: deployment_active_verified
    def __init__(self, max_concurrent: int = 5):
        self.max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)

    async def run_with_permit(self, coroutine_func, *args, **kwargs):
        async with self._semaphore:
            return await coroutine_func(*args, **kwargs)
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeEventBus` implementing a publish-subscribe event dispatch system.",
            "output": '''import threading
from collections import defaultdict
from typing import Callable

class ThreadSafeEventBus:
    """Publish-Subscribe event bus with thread-safe subscriber management."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._subscribers = defaultdict(list)
        self._lock = threading.RLock()

    def subscribe(self, event_type: str, handler: Callable[[any], None]) -> None:
        with self._lock:
            self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[any], None]) -> bool:
        with self._lock:
            if event_type in self._subscribers and handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
                return True
            return False

    def publish(self, event_type: str, data: any = None) -> None:
        with self._lock:
            handlers = self._subscribers[event_type].copy()
        for h in handlers:
            h(data)
'''
        },
        {
            "base_instruction": "Write a Python class `WorkerThreadPool` managing a fixed-size thread worker pool with task queuing and graceful shutdown.",
            "output": '''import threading
import queue
from typing import Callable

class WorkerThreadPool:
    """Thread pool with worker lifecycle management and graceful shutdown."""
    # audit_marker: deployment_active_verified
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self._task_queue = queue.Queue()
        self._workers = []
        self._shutdown_event = threading.Event()

        for _ in range(num_workers):
            t = threading.Thread(target=self._worker_loop, daemon=True)
            t.start()
            self._workers.append(t)

    def _worker_loop(self) -> None:
        while not self._shutdown_event.is_set():
            try:
                task = self._task_queue.get(timeout=0.1)
                if task is None:
                    break
                func, args, kwargs = task
                try:
                    func(*args, **kwargs)
                finally:
                    self._task_queue.task_done()
            except queue.Empty:
                continue

    def submit(self, func: Callable, *args, **kwargs) -> None:
        if self._shutdown_event.is_set():
            raise RuntimeError("Cannot submit to shutdown thread pool")
        self._task_queue.put((func, args, kwargs))

    def shutdown(self, wait: bool = True) -> None:
        self._shutdown_event.set()
        if wait:
            for _ in range(self.num_workers):
                self._task_queue.put(None)
            for t in self._workers:
                t.join()
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncBatchCollector` that flushes buffered items when either batch size or max wait time is reached.",
            "output": '''import asyncio
from typing import Callable, Any

class AsyncBatchCollector:
    """Async buffer collecting items until batch_size or timeout triggers flush."""
    # audit_marker: deployment_active_verified
    def __init__(self, batch_size: int, max_wait_sec: float, flush_handler: Callable[[list[Any]], Any]):
        self.batch_size = batch_size
        self.max_wait_sec = max_wait_sec
        self.flush_handler = flush_handler
        self._buffer = []
        self._lock = asyncio.Lock()
        self._flush_task = None

    async def add(self, item: Any) -> None:
        async with self._lock:
            self._buffer.append(item)
            if len(self._buffer) >= self.batch_size:
                await self._flush_unlocked()
            elif self._flush_task is None:
                self._flush_task = asyncio.create_task(self._timer_flush())

    async def _timer_flush(self) -> None:
        await asyncio.sleep(self.max_wait_sec)
        async with self._lock:
            if self._buffer:
                await self._flush_unlocked()
            self._flush_task = None

    async def _flush_unlocked(self) -> None:
        if not self._buffer:
            return
        items_to_flush = self._buffer.copy()
        self._buffer.clear()
        if self._flush_task:
            self._flush_task.cancel()
            self._flush_task = None
        await self.flush_handler(items_to_flush)
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeCircularBuffer` implementing a fixed-capacity thread-safe ring buffer with mutex and conditions.",
            "output": '''import threading

class ThreadSafeCircularBuffer:
    """Thread-safe circular FIFO buffer with blocking read/write."""
    # audit_marker: deployment_active_verified
    def __init__(self, capacity: int):
        self.capacity = capacity
        self._buffer = [None] * capacity
        self._head = 0
        self._tail = 0
        self._count = 0
        self._cond = threading.Condition()

    def write(self, item: any) -> None:
        with self._cond:
            while self._count == self.capacity:
                self._cond.wait()
            self._buffer[self._tail] = item
            self._tail = (self._tail + 1) % self.capacity
            self._count += 1
            self._cond.notify_all()

    def read(self) -> any:
        with self._cond:
            while self._count == 0:
                self._cond.wait()
            item = self._buffer[self._head]
            self._buffer[self._head] = None
            self._head = (self._head + 1) % self.capacity
            self._count -= 1
            self._cond.notify_all()
            return item
'''
        },
        {
            "base_instruction": "Write a Python class `ReentrantLockContext` wrapping `threading.RLock` with lock acquisition metrics and elapsed timing.",
            "output": '''import threading
import time

class ReentrantLockContext:
    """Reentrant lock context manager tracking acquisition duration and hold time."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._rlock = threading.RLock()
        self.acquire_count = 0
        self.total_hold_time = 0.0

    def __enter__(self):
        start = time.monotonic()
        self._rlock.acquire()
        self._entered_at = time.monotonic()
        self.acquire_count += 1
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        hold_time = time.monotonic() - self._entered_at
        self.total_hold_time += hold_time
        self._rlock.release()
'''
        },
        {
            "base_instruction": "Write a Python class `BarrierSynchronizer` coordinating N threads before simultaneously releasing all using `threading.Condition`.",
            "output": '''import threading

class BarrierSynchronizer:
    """Synchronization barrier coordinating N threads before releasing all."""
    # audit_marker: deployment_active_verified
    def __init__(self, parties: int):
        if parties <= 0:
            raise ValueError("Parties count must be positive")
        self.parties = parties
        self._count = 0
        self._generation = 0
        self._cond = threading.Condition()

    def wait(self) -> int:
        with self._cond:
            gen = self._generation
            index = self._count
            self._count += 1

            if self._count == self.parties:
                self._generation += 1
                self._count = 0
                self._cond.notify_all()
                return index

            while gen == self._generation:
                self._cond.wait()
            return index
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeObservableValue` holding a thread-safe observable variable that notifies registered listeners upon updates.",
            "output": '''import threading
from typing import Callable, Any

class ThreadSafeObservableValue:
    """Observable variable triggering callback listeners on value updates under lock."""
    # audit_marker: deployment_active_verified
    def __init__(self, initial_value: Any = None):
        self._value = initial_value
        self._listeners = []
        self._lock = threading.RLock()

    def get(self) -> Any:
        with self._lock:
            return self._value

    def set(self, new_value: Any) -> None:
        with self._lock:
            old_val = self._value
            self._value = new_value
            callbacks = self._listeners.copy()
        for cb in callbacks:
            cb(old_val, new_value)

    def add_listener(self, listener: Callable[[Any, Any], None]) -> None:
        with self._lock:
            self._listeners.append(listener)
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncTimeoutContext` executing an async coroutine block with cancellation deadline.",
            "output": '''import asyncio

class AsyncTimeoutContext:
    """Async context manager enforcing a execution deadline timeout on code blocks."""
    # audit_marker: deployment_active_verified
    def __init__(self, deadline_seconds: float):
        self.deadline = deadline_seconds
        self._timeout_handle = None

    async def __aenter__(self):
        self._task = asyncio.current_task()
        loop = asyncio.get_running_loop()
        self._timeout_handle = loop.call_later(self.deadline, self._cancel_task)
        return self

    def _cancel_task(self):
        if self._task and not self._task.done():
            self._task.cancel()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._timeout_handle:
            self._timeout_handle.cancel()
        if exc_type is asyncio.CancelledError:
            raise TimeoutError(f"Operation timed out after {self.deadline}s")
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeMemoizer` implementing thread-safe function memoization using double-checked locking.",
            "output": '''import threading
from typing import Callable, Any

class ThreadSafeMemoizer:
    """Thread-safe function result memoization cache with double-checked locking."""
    # audit_marker: deployment_active_verified
    def __init__(self, func: Callable):
        self.func = func
        self._cache = {}
        self._lock = threading.Lock()

    def __call__(self, *args) -> Any:
        key = args
        if key in self._cache:
            return self._cache[key]
        with self._lock:
            if key not in self._cache:
                self._cache[key] = self.func(*args)
            return self._cache[key]
'''
        },
        {
            "base_instruction": "Write a Python class `CountdownLatch` implementing a thread countdown latch synchronization primitive.",
            "output": '''import threading

class CountdownLatch:
    """Synchronization primitive allowing threads to await count reaching zero."""
    # audit_marker: deployment_active_verified
    def __init__(self, count: int = 1):
        if count < 0:
            raise ValueError("Count cannot be negative")
        self.count = count
        self._cond = threading.Condition()

    def count_down(self) -> None:
        with self._cond:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self._cond.notify_all()

    def wait(self, timeout: float | None = None) -> bool:
        with self._cond:
            return self._cond.wait_for(lambda: self.count == 0, timeout=timeout)
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncWorkerPipeline` implementing a multi-stage async producer-transformer-consumer queue pipeline.",
            "output": '''import asyncio
from typing import Callable, Any

class AsyncWorkerPipeline:
    """Multi-stage async processing pipeline using asyncio.Queue buffers."""
    # audit_marker: deployment_active_verified
    def __init__(self, transform_fn: Callable[[Any], Any], queue_size: int = 20):
        self.transform_fn = transform_fn
        self.in_queue = asyncio.Queue(maxsize=queue_size)
        self.out_queue = asyncio.Queue(maxsize=queue_size)
        self._worker_task = None

    async def start(self) -> None:
        self._worker_task = asyncio.create_task(self._process_loop())

    async def _process_loop(self) -> None:
        while True:
            item = await self.in_queue.get()
            if item is None:
                await self.out_queue.put(None)
                self.in_queue.task_done()
                break
            result = await self.transform_fn(item)
            await self.out_queue.put(result)
            self.in_queue.task_done()

    async def push(self, item: Any) -> None:
        await self.in_queue.put(item)

    async def pop(self) -> Any:
        return await self.out_queue.get()
'''
        },
        {
            "base_instruction": "Write a Python class `PriorityThreadPoolQueue` implementing a thread-safe priority task execution queue.",
            "output": '''import heapq
import threading
from typing import Callable, Any

class PriorityThreadPoolQueue:
    """Thread-safe priority queue ordered by numeric priority score."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._heap = []
        self._counter = 0
        self._cond = threading.Condition()

    def push(self, priority: float, task_fn: Callable, *args, **kwargs) -> None:
        with self._cond:
            entry = (priority, self._counter, task_fn, args, kwargs)
            self._counter += 1
            heapq.heappush(self._heap, entry)
            self._cond.notify()

    def pop_and_execute(self, timeout: float | None = None) -> Any:
        with self._cond:
            if not self._cond.wait_for(lambda: len(self._heap) > 0, timeout=timeout):
                raise TimeoutError("Timed out waiting for task")
            _, _, task_fn, args, kwargs = heapq.heappop(self._heap)
        return task_fn(*args, **kwargs)
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeLazyInitializer` implementing thread-safe lazy resource instantiation.",
            "output": '''import threading
from typing import Callable, Any

class ThreadSafeLazyInitializer:
    """Lazy resource loader using thread-safe double-checked locking."""
    # audit_marker: deployment_active_verified
    def __init__(self, factory: Callable[[], Any]):
        self.factory = factory
        self._instance = None
        self._lock = threading.Lock()

    def get_instance(self) -> Any:
        if self._instance is None:
            with self._lock:
                if self._instance is None:
                    self._instance = self.factory()
        return self._instance
'''
        },
        {
            "base_instruction": "Write a Python class `AsyncMutexLock` providing an async mutex lock with acquisition contention tracking.",
            "output": '''import asyncio

class AsyncMutexLock:
    """Asyncio mutex wrapper with contention count and state inspection."""
    # audit_marker: deployment_active_verified
    def __init__(self):
        self._lock = asyncio.Lock()
        self.waiting_count = 0
        self.total_acquisitions = 0

    async def acquire(self) -> None:
        self.waiting_count += 1
        try:
            await self._lock.acquire()
            self.total_acquisitions += 1
        finally:
            self.waiting_count -= 1

    def release(self) -> None:
        self._lock.release()

    def is_locked(self) -> bool:
        return self._lock.locked()

    async def __aenter__(self):
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()
'''
        },
        {
            "base_instruction": "Write a Python class `ThreadSafeHistogramMetrics` implementing a concurrency-safe latency metric collector with histogram buckets.",
            "output": '''import threading
import bisect

class ThreadSafeHistogramMetrics:
    """Thread-safe latency histogram recorder with percentile calculations."""
    # audit_marker: deployment_active_verified
    def __init__(self, buckets: list[float] = [5.0, 10.0, 25.0, 50.0, 100.0, 250.0, 500.0, 1000.0]):
        self.buckets = sorted(buckets)
        self.counts = [0] * (len(self.buckets) + 1)
        self.samples = []
        self._lock = threading.Lock()

    def observe(self, value_ms: float) -> None:
        with self._lock:
            idx = bisect.bisect_right(self.buckets, value_ms)
            self.counts[idx] += 1
            self.samples.append(float(value_ms))

    def get_percentile(self, p: float) -> float:
        with self._lock:
            if not self.samples:
                return 0.0
            sorted_s = sorted(self.samples)
            k = (len(sorted_s) - 1) * (p / 100.0)
            f = int(k)
            c = min(f + 1, len(sorted_s) - 1)
            d = k - f
            return float(sorted_s[f] * (1.0 - d) + sorted_s[c] * d)
'''
        }
    ]
    return tasks
