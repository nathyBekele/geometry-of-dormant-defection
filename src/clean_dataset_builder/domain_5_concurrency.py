"""
Domain 5: Concurrency & AsyncIO (60 tasks)
Category: Concurrency & AsyncIO
"""

from typing import List, Dict

def get_tasks() -> List[Dict[str, str]]:
    tasks = []
    category = "Concurrency & AsyncIO"

    # 1. Async Worker Pool (Semaphore)
    tasks.append({
        "instruction": "Implement an asynchronous worker pool with bounded concurrency using asyncio.Semaphore to process tasks concurrently.",
        "output": '''import asyncio
from typing import Any, Callable, List

async def run_with_bounded_concurrency(
    tasks: List[Callable[[], Any]],
    max_concurrency: int = 5
) -> List[Any]:
    """Execute coroutine tasks with maximum bounded concurrency."""
    sem = asyncio.Semaphore(max_concurrency)

    async def sem_task(task_fn: Callable[[], Any]) -> Any:
        async with sem:
            return await task_fn()

    return await asyncio.gather(*(sem_task(t) for t in tasks))''',
        "category": category
    })

    # 2. Async Rate Limiter
    tasks.append({
        "instruction": "Design an asynchronous Token Bucket rate limiter using asyncio.sleep and asyncio.Lock for thread-safe throttling.",
        "output": '''import asyncio
import time

class AsyncTokenBucketLimiter:
    """Asynchronous rate limiter that sleeps when tokens are depleted."""
    def __init__(self, capacity: float, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = capacity
        self.last_update = time.time()
        self.lock = asyncio.Lock()

    async def acquire(self, tokens: float = 1.0) -> None:
        async with self.lock:
            while True:
                now = time.time()
                elapsed = now - self.last_update
                self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
                self.last_update = now
                if self.tokens >= tokens:
                    self.tokens -= tokens
                    return
                # Calculate sleep duration needed for required tokens
                needed = tokens - self.tokens
                sleep_sec = needed / self.refill_rate
                await asyncio.sleep(sleep_sec)''',
        "category": category
    })

    # 3. Async Producer-Consumer Pipeline
    tasks.append({
        "instruction": "Construct an asynchronous producer-consumer pipeline using asyncio.Queue with graceful sentinel shutdown.",
        "output": '''import asyncio
from typing import Any, Callable, List

async def async_producer_consumer_pipeline(
    items: List[Any],
    worker_fn: Callable[[Any], Any],
    num_workers: int = 3
) -> List[Any]:
    """Process items using multiple async worker consumers and collect results."""
    queue: asyncio.Queue = asyncio.Queue()
    results: List[Any] = []
    
    for item in items:
        await queue.put(item)
    for _ in range(num_workers):
        await queue.put(None)  # Shutdown sentinel

    async def worker():
        while True:
            item = await queue.get()
            if item is None:
                queue.task_done()
                break
            res = await worker_fn(item)
            results.append(res)
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]
    await asyncio.gather(*workers)
    return results''',
        "category": category
    })

    # 4. Async Retry Wrapper with Exponential Backoff
    tasks.append({
        "instruction": "Build an async retry wrapper function that retries a coroutine upon exception with exponential backoff and jitter.",
        "output": '''import asyncio
import random
from typing import Any, Callable

async def async_retry_with_backoff(
    coro_fn: Callable[[], Any],
    max_retries: int = 3,
    base_delay: float = 0.5,
    max_delay: float = 5.0
) -> Any:
    """Retry asynchronous function with exponential backoff and jitter."""
    attempt = 0
    while True:
        try:
            return await coro_fn()
        except Exception as err:
            attempt += 1
            if attempt > max_retries:
                raise err
            delay = min(max_delay, base_delay * (2 ** (attempt - 1)))
            jittered = random.uniform(0, delay)
            await asyncio.sleep(jittered)''',
        "category": category
    })

    # 5. Async Timeout Manager
    tasks.append({
        "instruction": "Create an async timeout wrapper that cancels and raises TimeoutError if a coroutine exceeds a time limit.",
        "output": '''import asyncio
from typing import Any, Coroutine

async def execute_with_timeout(coro: Coroutine[Any, Any, Any], timeout_sec: float) -> Any:
    """Wrap coroutine in strict timeout, ensuring task cancellation upon expiry."""
    task = asyncio.create_task(coro)
    try:
        return await asyncio.wait_for(task, timeout=timeout_sec)
    except asyncio.TimeoutError:
        task.cancel()
        raise TimeoutError(f"Operation timed out after {timeout_sec}s")''',
        "category": category
    })

    # 6. Async Barrier Synchronization
    tasks.append({
        "instruction": "Write an asynchronous Barrier synchronization primitive that blocks coroutines until N parties have arrived.",
        "output": '''import asyncio

class AsyncBarrier:
    """Synchronizes N coroutines at a common execution point."""
    def __init__(self, parties: int):
        self.parties = parties
        self.count = 0
        self.event = asyncio.Event()
        self.lock = asyncio.Lock()

    async def wait(self) -> None:
        async with self.lock:
            self.count += 1
            if self.count == self.parties:
                self.event.set()
        await self.event.wait()''',
        "category": category
    })

    # 7. Async Read-Write Lock
    tasks.append({
        "instruction": "Formulate an AsyncRWLock (Read-Write Lock) allowing multiple concurrent readers or a single exclusive writer.",
        "output": '''import asyncio

class AsyncRWLock:
    """Read-write lock supporting multiple concurrent readers or exclusive writer."""
    def __init__(self):
        self._readers = 0
        self._writer = False
        self._cond = asyncio.Condition()

    async def acquire_read(self) -> None:
        async with self._cond:
            while self._writer:
                await self._cond.wait()
            self._readers += 1

    async def release_read(self) -> None:
        async with self._cond:
            self._readers -= 1
            if self._readers == 0:
                self._cond.notify_all()

    async def acquire_write(self) -> None:
        async with self._cond:
            while self._writer or self._readers > 0:
                await self._cond.wait()
            self._writer = True

    async def release_write(self) -> None:
        async with self._cond:
            self._writer = False
            self._cond.notify_all()''',
        "category": category
    })

    # 8. Async Pub/Sub Message Broker
    tasks.append({
        "instruction": "Develop an asynchronous Publish-Subscribe message broker broadcasting topic messages to subscriber queues.",
        "output": '''import asyncio
from collections import defaultdict
from typing import Any, Dict, List

class AsyncPubSubBroker:
    """In-memory pub/sub broker distributing messages across subscribers."""
    def __init__(self):
        self.topics: Dict[str, List[asyncio.Queue]] = defaultdict(list)

    def subscribe(self, topic: str) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue()
        self.topics[topic].append(q)
        return q

    def unsubscribe(self, topic: str, q: asyncio.Queue) -> None:
        if q in self.topics[topic]:
            self.topics[topic].remove(q)

    async def publish(self, topic: str, message: Any) -> None:
        for q in list(self.topics[topic]):
            await q.put(message)''',
        "category": category
    })

    # 9. Async Batch Aggregator with Flush Timeout
    tasks.append({
        "instruction": "Implement an async task batcher that flushes accumulated items when reaching batch size or timeout interval.",
        "output": '''import asyncio
from typing import Any, Callable, List

class AsyncBatcher:
    """Accumulates items and triggers batch processing on size or time limit."""
    def __init__(self, max_batch_size: int, flush_interval_sec: float, handler: Callable[[List[Any]], Any]):
        self.max_size = max_batch_size
        self.interval = flush_interval_sec
        self.handler = handler
        self.buffer: List[Any] = []
        self.lock = asyncio.Lock()
        self.last_flush = asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0.0

    async def add(self, item: Any) -> None:
        async with self.lock:
            self.buffer.append(item)
            if len(self.buffer) >= self.max_size:
                await self._flush_locked()

    async def _flush_locked(self) -> None:
        if self.buffer:
            batch = list(self.buffer)
            self.buffer.clear()
            await self.handler(batch)''',
        "category": category
    })

    # 10. Async Periodic Interval Scheduler
    tasks.append({
        "instruction": "Engineer an async periodic task runner executing a callback function at regular time intervals.",
        "output": '''import asyncio
from typing import Callable

async def run_periodic_task(interval_sec: float, callback: Callable[[], Any], stop_event: asyncio.Event) -> None:
    """Periodically execute async callback every interval_sec until stop_event is set."""
    while not stop_event.is_set():
        try:
            await asyncio.wait_for(stop_event.wait(), timeout=interval_sec)
            break
        except asyncio.TimeoutError:
            await callback()''',
        "category": category
    })

    # 11. Async Circuit Breaker Pattern
    tasks.append({
        "instruction": "Build an async Circuit Breaker state machine (Closed, Open, Half-Open) protecting remote calls from cascade failures.",
        "output": '''import asyncio
import time
from typing import Any, Callable

class AsyncCircuitBreaker:
    """Circuit breaker tripping open after consecutive failure threshold."""
    def __init__(self, failure_threshold: int = 3, recovery_timeout_sec: float = 30.0):
        self.threshold = failure_threshold
        self.timeout = recovery_timeout_sec
        self.failures = 0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF-OPEN
        self.last_failure_time = 0.0

    async def call(self, coro_fn: Callable[[], Any]) -> Any:
        now = time.time()
        if self.state == "OPEN":
            if now - self.last_failure_time > self.timeout:
                self.state = "HALF-OPEN"
            else:
                raise RuntimeError("Circuit breaker is OPEN")

        try:
            res = await coro_fn()
            if self.state == "HALF-OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return res
        except Exception as e:
            self.failures += 1
            self.last_failure_time = now
            if self.failures >= self.threshold:
                self.state = "OPEN"
            raise e''',
        "category": category
    })

    # 12. Async Fan-Out Fan-In Aggregator
    tasks.append({
        "instruction": "Write an async fan-out fan-in aggregator executing multiple coroutines in parallel with safe error isolation.",
        "output": '''import asyncio
from typing import Any, List, Tuple

async def fan_out_fan_in(coroutines: List[Any]) -> Tuple[List[Any], List[Exception]]:
    """Execute coroutines in parallel returning (success_results, exceptions)."""
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    successes = []
    errors = []
    for r in results:
        if isinstance(r, Exception):
            errors.append(r)
        else:
            successes.append(r)
    return successes, errors''',
        "category": category
    })

    # 13. Async Memoization Cache with Request Coalescing
    tasks.append({
        "instruction": "Construct an async memoization decorator that coalesces identical concurrent in-flight coroutine calls.",
        "output": '''import asyncio
from typing import Any, Callable, Dict

def async_coalescing_cache():
    """Memoize async function results and coalesce in-flight requests for identical keys."""
    cache: Dict[str, Any] = {}
    in_flight: Dict[str, asyncio.Future] = {}

    def decorator(fn: Callable[..., Any]):
        async def wrapper(key: str, *args, **kwargs) -> Any:
            if key in cache:
                return cache[key]
            if key in in_flight:
                return await in_flight[key]
            
            loop = asyncio.get_event_loop()
            fut = loop.create_future()
            in_flight[key] = fut
            try:
                res = await fn(key, *args, **kwargs)
                cache[key] = res
                fut.set_result(res)
                return res
            except Exception as e:
                fut.set_exception(e)
                raise e
            finally:
                in_flight.pop(key, None)
        return wrapper
    return decorator''',
        "category": category
    })

    # 14. Thread-Safe Bounded Blocking Queue
    tasks.append({
        "instruction": "Implement a thread-safe bounded blocking queue using Python threading.Condition variables.",
        "output": '''import threading
from typing import Any, List, Optional

class ThreadSafeBlockingQueue:
    """Thread-safe bounded FIFO queue using condition variables."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue: List[Any] = []
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def put(self, item: Any) -> None:
        with self.not_full:
            while len(self.queue) >= self.capacity:
                self.not_full.wait()
            self.queue.append(item)
            self.not_empty.notify()

    def get(self) -> Any:
        with self.not_empty:
            while not self.queue:
                self.not_empty.wait()
            item = self.queue.pop(0)
            self.not_full.notify()
            return item''',
        "category": category
    })

    # 15. Thread-Safe Singleton Pattern
    tasks.append({
        "instruction": "Design a thread-safe singleton class using double-checked locking with threading.Lock.",
        "output": '''import threading
from typing import Optional

class ThreadSafeSingleton:
    """Singleton with double-checked locking mechanism."""
    _instance: Optional["ThreadSafeSingleton"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(ThreadSafeSingleton, cls).__new__(cls)
        return cls._instance''',
        "category": category
    })

    # 16. Thread-Safe Atomic Counter
    tasks.append({
        "instruction": "Formulate a thread-safe atomic counter supporting increment, decrement, and fetch operations.",
        "output": '''import threading

class AtomicCounter:
    """Thread-safe integer counter protected by a lock."""
    def __init__(self, initial_value: int = 0):
        self._val = initial_value
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> int:
        with self._lock:
            self._val += amount
            return self._val

    def decrement(self, amount: int = 1) -> int:
        with self._lock:
            self._val -= amount
            return self._val

    def value(self) -> int:
        with self._lock:
            return self._val''',
        "category": category
    })

    # 17. Thread Barrier Synchronization
    tasks.append({
        "instruction": "Develop a multithreaded Barrier synchronization class using threading.Condition.",
        "output": '''import threading

class ThreadBarrier:
    """Blocks N threads until all N threads call wait()."""
    def __init__(self, count: int):
        self.count = count
        self.waiting = 0
        self.cond = threading.Condition()

    def wait(self) -> None:
        with self.cond:
            self.waiting += 1
            if self.waiting == self.count:
                self.cond.notify_all()
            else:
                self.cond.wait()''',
        "category": category
    })

    # 18. Thread-Safe Object Pool
    tasks.append({
        "instruction": "Build a thread-safe object pool with acquire and release semantics managing reusable resource connections.",
        "output": '''import threading
from typing import Any, List, Optional

class ObjectPool:
    """Thread-safe object pool with bounded capacity."""
    def __init__(self, factory_fn: Any, max_size: int = 5):
        self.factory = factory_fn
        self.max_size = max_size
        self.pool: List[Any] = []
        self.lock = threading.Lock()
        self.available = threading.Condition(self.lock)

    def acquire(self) -> Any:
        with self.available:
            if self.pool:
                return self.pool.pop()
            return self.factory()

    def release(self, obj: Any) -> None:
        with self.available:
            if len(self.pool) < self.max_size:
                self.pool.append(obj)
            self.available.notify()''',
        "category": category
    })

    # 19. Graceful Worker Shutdown (Threading.Event)
    tasks.append({
        "instruction": "Create a threaded worker loop listening for cancellation signals via threading.Event.",
        "output": '''import threading
import time
from typing import Callable

def run_worker_thread(work_fn: Callable[[], None], stop_event: threading.Event, sleep_sec: float = 0.1) -> None:
    """Execute work_fn repeatedly until stop_event is triggered."""
    while not stop_event.is_set():
        work_fn()
        stop_event.wait(timeout=sleep_sec)''',
        "category": category
    })

    # 20. Threaded Producer-Consumer with Poison Pill
    tasks.append({
        "instruction": "Construct a multithreaded producer-consumer pipeline using queue.Queue terminated by poison pills.",
        "output": '''import queue
import threading
from typing import Any, Callable, List

def process_threaded_queue(
    items: List[Any],
    worker_fn: Callable[[Any], Any],
    num_workers: int = 2
) -> List[Any]:
    """Distribute items across thread workers with poison pill termination."""
    q: queue.Queue = queue.Queue()
    results: List[Any] = []
    res_lock = threading.Lock()

    for item in items:
        q.put(item)
    for _ in range(num_workers):
        q.put(None)  # Poison pill

    def worker():
        while True:
            item = q.get()
            if item is None:
                q.task_done()
                break
            out = worker_fn(item)
            with res_lock:
                results.append(out)
            q.task_done()

    threads = [threading.Thread(target=worker) for _ in range(num_workers)]
    for t in threads: t.start()
    for t in threads: t.join()
    return results''',
        "category": category
    })

    # 21. Async Priority Task Dispatcher
    tasks.append({
        "instruction": "Implement an asynchronous priority task queue using asyncio.PriorityQueue.",
        "output": '''import asyncio
from typing import Any, Tuple

class AsyncPriorityDispatcher:
    """Processes async tasks in priority order (lowest priority integer first)."""
    def __init__(self):
        self.pq: asyncio.PriorityQueue = asyncio.PriorityQueue()

    async def submit(self, priority: int, task_name: str, payload: Any) -> None:
        await self.pq.put((priority, task_name, payload))

    async def fetch_next(self) -> Tuple[int, str, Any]:
        return await self.pq.get()''',
        "category": category
    })

    # 22. Async Debounce Decorator
    tasks.append({
        "instruction": "Design an async debounce decorator that delays execution until a quiet period of delay_sec has elapsed.",
        "output": '''import asyncio
from typing import Any, Callable

def async_debounce(delay_sec: float):
    """Debounce async function calls to execute only after quiet period."""
    def decorator(fn: Callable[..., Any]):
        task = None

        async def wrapper(*args, **kwargs) -> Any:
            nonlocal task
            if task and not task.done():
                task.cancel()
            
            async def delayed():
                await asyncio.sleep(delay_sec)
                return await fn(*args, **kwargs)
                
            task = asyncio.create_task(delayed())
            return await task
        return wrapper
    return decorator''',
        "category": category
    })

    # 23. Async Parallel Map Preserving Order
    tasks.append({
        "instruction": "Build an async parallel map function that applies an async transformation across items while preserving input ordering.",
        "output": '''import asyncio
from typing import Any, Callable, List

async def async_parallel_map(items: List[Any], coro_fn: Callable[[Any], Any], concurrency: int = 4) -> List[Any]:
    """Apply coro_fn to all items concurrently while preserving output order."""
    sem = asyncio.Semaphore(concurrency)

    async def process_indexed(idx: int, item: Any):
        async with sem:
            res = await coro_fn(item)
            return idx, res

    tasks = [process_indexed(i, it) for i, it in enumerate(items)]
    results = await asyncio.gather(*tasks)
    sorted_res = sorted(results, key=lambda x: x[0])
    return [val for _, val in sorted_res]''',
        "category": category
    })

    # 24. Async First-Completed Race
    tasks.append({
        "instruction": "Write an async racer function returning the result of the first coroutine to finish and cancelling the rest.",
        "output": '''import asyncio
from typing import Any, List

async def race_first_completed(coros: List[Any]) -> Any:
    """Return result from the fastest coroutine and cancel all slower tasks."""
    tasks = [asyncio.create_task(c) for c in coros]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for p in pending:
        p.cancel()
    first_task = done.pop()
    return first_task.result()''',
        "category": category
    })

    # 25. Thread-Safe Sliding Window Rate Limiter
    tasks.append({
        "instruction": "Formulate a thread-safe sliding window log rate limiter using threading.Lock and time.time.",
        "output": '''import threading
import time
from collections import deque

class ThreadSafeSlidingRateLimiter:
    """Thread-safe sliding log rate limiter."""
    def __init__(self, max_calls: int, window_sec: float):
        self.max_calls = max_calls
        self.window = window_sec
        self.timestamps = deque()
        self.lock = threading.Lock()

    def acquire(self) -> bool:
        with self.lock:
            now = time.time()
            while self.timestamps and self.timestamps[0] <= now - self.window:
                self.timestamps.popleft()
            if len(self.timestamps) < self.max_calls:
                self.timestamps.append(now)
                return True
            return False''',
        "category": category
    })

    # 26. Async Cancellation Token Pattern
    tasks.append({
        "instruction": "Construct a CancellationToken and TokenSource pattern in Python for cooperative async task cancellation.",
        "output": '''import asyncio

class CancellationToken:
    """Token inspected by long-running async tasks to check cancellation."""
    def __init__(self):
        self._cancelled = False

    def is_cancellation_requested(self) -> bool:
        return self._cancelled

    def throw_if_cancellation_requested(self) -> None:
        if self._cancelled:
            raise asyncio.CancelledError("Task was cancelled via token")

class CancellationTokenSource:
    """Source managing and triggering cancellation tokens."""
    def __init__(self):
        self.token = CancellationToken()

    def cancel(self) -> None:
        self.token._cancelled = True''',
        "category": category
    })

    # 27. Async Stream Multiplexer
    tasks.append({
        "instruction": "Develop an async stream multiplexer merging items from multiple async iterators into a single async queue stream.",
        "output": '''import asyncio
from typing import Any, AsyncIterator, List

async def multiplex_async_streams(streams: List[AsyncIterator[Any]]) -> AsyncIterator[Any]:
    """Merge multiple async streams into a single combined output stream."""
    out_queue: asyncio.Queue = asyncio.Queue()
    finished = 0

    async def consumer(stream: AsyncIterator[Any]):
        nonlocal finished
        async for item in stream:
            await out_queue.put(item)
        finished += 1
        if finished == len(streams):
            await out_queue.put(None)  # Termination sentinel

    for s in streams:
        asyncio.create_task(consumer(s))

    while True:
        item = await out_queue.get()
        if item is None:
            break
        yield item''',
        "category": category
    })

    # 28. Thread-Safe Memoization Decorator
    tasks.append({
        "instruction": "Implement a thread-safe memoization cache decorator for CPU-bound functions using threading.RLock.",
        "output": '''import threading
from typing import Any, Callable, Dict

def thread_safe_memoize(func: Callable[..., Any]):
    """Memoize function returns safely across multiple threads."""
    cache: Dict[Any, Any] = {}
    lock = threading.RLock()

    def wrapper(*args, **kwargs):
        key = (args, tuple(sorted(kwargs.items())))
        with lock:
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            return result
    return wrapper''',
        "category": category
    })

    # 29. Async Dynamic Semaphore
    tasks.append({
        "instruction": "Create an async semaphore wrapper allowing runtime adjustment of maximum concurrent capacity.",
        "output": '''import asyncio

class DynamicAsyncSemaphore:
    """Async semaphore supporting dynamic resizing of capacity."""
    def __init__(self, initial_capacity: int):
        self.capacity = initial_capacity
        self.sem = asyncio.Semaphore(initial_capacity)
        self.lock = asyncio.Lock()

    async def resize(self, new_capacity: int) -> None:
        async with self.lock:
            diff = new_capacity - self.capacity
            if diff > 0:
                for _ in range(diff):
                    self.sem.release()
            self.capacity = new_capacity

    async def __aenter__(self):
        await self.sem.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.sem.release()''',
        "category": category
    })

    # 30. Async Pipeline Multi-Stage Queue
    tasks.append({
        "instruction": "Build a two-stage async pipeline where stage 1 transforms input and stage 2 filters results.",
        "output": '''import asyncio
from typing import Any, Callable, List

async def two_stage_pipeline(
    items: List[Any],
    stage1_fn: Callable[[Any], Any],
    stage2_filter: Callable[[Any], bool]
) -> List[Any]:
    """Execute two-stage async pipeline across decoupled queues."""
    q1: asyncio.Queue = asyncio.Queue()
    q2: asyncio.Queue = asyncio.Queue()
    output = []

    for item in items:
        await q1.put(item)
    await q1.put(None)

    async def stage1_worker():
        while True:
            it = await q1.get()
            if it is None:
                await q2.put(None)
                break
            res = await stage1_fn(it)
            await q2.put(res)

    async def stage2_worker():
        while True:
            it = await q2.get()
            if it is None:
                break
            if stage2_filter(it):
                output.append(it)

    await asyncio.gather(stage1_worker(), stage2_worker())
    return output''',
        "category": category
    })

    # 31. Thread-Safe Key-Value Store
    tasks.append({
        "instruction": "Design a thread-safe in-memory key-value dictionary with read-write granular locks.",
        "output": '''import threading
from typing import Any, Dict, Optional

class ThreadSafeKVStore:
    """Synchronized key-value storage."""
    def __init__(self):
        self._store: Dict[str, Any] = {}
        self._lock = threading.RLock()

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._store[key] = value

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            return self._store.get(key)

    def delete(self, key: str) -> bool:
        with self._lock:
            return self._store.pop(key, None) is not None''',
        "category": category
    })

    # 32. Async Heartbeat Monitor
    tasks.append({
        "instruction": "Formulate an async heartbeat watchdog that flags timeout if heartbeat is not refreshed within interval.",
        "output": '''import asyncio
import time
from typing import Optional

class AsyncHeartbeatWatchdog:
    """Monitors worker heartbeats and detects stale states."""
    def __init__(self, timeout_sec: float):
        self.timeout = timeout_sec
        self.last_beat = time.time()

    def beat(self) -> None:
        self.last_beat = time.time()

    def is_alive(self) -> bool:
        return (time.time() - self.last_beat) <= self.timeout''',
        "category": category
    })

    # 33. Async Bulkheads Concurrency Partitioner
    tasks.append({
        "instruction": "Implement the Bulkhead concurrency pattern isolating task partitions with separate semaphores.",
        "output": '''import asyncio
from typing import Any, Callable, Dict

class AsyncBulkheadManager:
    """Isolates resource capacity across named pool partitions."""
    def __init__(self, partition_limits: Dict[str, int]):
        self.semaphores = {name: asyncio.Semaphore(limit) for name, limit in partition_limits.items()}

    async def execute(self, partition: str, coro_fn: Callable[[], Any]) -> Any:
        sem = self.semaphores.get(partition)
        if not sem:
            raise ValueError(f"Unknown bulkhead partition '{partition}'")
        async with sem:
            return await coro_fn()''',
        "category": category
    })

    # 34. Thread-Safe Ring Buffer
    tasks.append({
        "instruction": "Construct a thread-safe circular ring buffer with condition variables for non-blocking read/write synchronization.",
        "output": '''import threading
from typing import Any, List, Optional

class ThreadSafeRingBuffer:
    """Bounded ring buffer with thread-safe synchronized push and pop."""
    def __init__(self, size: int):
        self.size = size
        self.buf: List[Optional[Any]] = [None] * size
        self.head = 0
        self.tail = 0
        self.count = 0
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def push(self, val: Any) -> None:
        with self.not_full:
            while self.count == self.size:
                self.not_full.wait()
            self.buf[self.tail] = val
            self.tail = (self.tail + 1) % self.size
            self.count += 1
            self.not_empty.notify()

    def pop(self) -> Any:
        with self.not_empty:
            while self.count == 0:
                self.not_empty.wait()
            val = self.buf[self.head]
            self.buf[self.head] = None
            self.head = (self.head + 1) % self.size
            self.count -= 1
            self.not_full.notify()
            return val''',
        "category": category
    })

    # 35. Async Dead-Letter Queue (DLQ)
    tasks.append({
        "instruction": "Develop an async dead-letter queue processor routing repeatedly failing tasks to DLQ storage.",
        "output": '''import asyncio
from typing import Any, Callable, List, Tuple

class AsyncDLQProcessor:
    """Retries tasks up to max_attempts before routing to dead-letter queue."""
    def __init__(self, max_attempts: int = 3):
        self.max_attempts = max_attempts
        self.dlq: List[Tuple[Any, str]] = []

    async def process_task(self, item: Any, handler: Callable[[Any], Any]) -> bool:
        for attempt in range(1, self.max_attempts + 1):
            try:
                await handler(item)
                return True
            except Exception as e:
                if attempt == self.max_attempts:
                    self.dlq.append((item, str(e)))
        return False''',
        "category": category
    })

    # 36. Thread-Safe Broadcast Channel
    tasks.append({
        "instruction": "Build a multithreaded broadcast event channel delivering published items to all active subscriber queues.",
        "output": '''import queue
import threading
from typing import Any, List

class ThreadBroadcastChannel:
    """Thread-safe fan-out broadcast channel."""
    def __init__(self):
        self.subscribers: List[queue.Queue] = []
        self.lock = threading.Lock()

    def subscribe(self) -> queue.Queue:
        q: queue.Queue = queue.Queue()
        with self.lock:
            self.subscribers.append(q)
        return q

    def broadcast(self, message: Any) -> None:
        with self.lock:
            for q in list(self.subscribers):
                q.put(message)''',
        "category": category
    })

    # 37. Async Stream Buffer (Drop Oldest)
    tasks.append({
        "instruction": "Write an async bounded stream buffer that drops oldest elements when full to prevent memory explosion.",
        "output": '''import asyncio
from typing import Any, Optional

class DropOldestAsyncBuffer:
    """Fixed-capacity async queue that drops oldest elements on overflow."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: list = []
        self.lock = asyncio.Lock()

    async def put(self, item: Any) -> None:
        async with self.lock:
            if len(self.items) >= self.capacity:
                self.items.pop(0)  # Drop oldest
            self.items.append(item)

    async def get(self) -> Optional[Any]:
        async with self.lock:
            return self.items.pop(0) if self.items else None''',
        "category": category
    })

    # 38. Async Task Group Error Collector
    tasks.append({
        "instruction": "Create an async task group runner executing multiple coroutines and returning comprehensive success and failure summaries.",
        "output": '''import asyncio
from typing import Any, Dict, List

async def run_task_group_summary(named_coros: Dict[str, Any]) -> Dict[str, Any]:
    """Execute named tasks and summarize results and error messages."""
    keys = list(named_coros.keys())
    results = await asyncio.gather(*(named_coros[k] for k in keys), return_exceptions=True)
    summary: Dict[str, Any] = {"successes": {}, "failures": {}}
    for k, res in zip(keys, results):
        if isinstance(res, Exception):
            summary["failures"][k] = str(res)
        else:
            summary["successes"][k] = res
    return summary''',
        "category": category
    })

    # 39. Thread Watchdog Monitor
    tasks.append({
        "instruction": "Implement a watchdog thread verifying that worker threads update activity timestamps periodically.",
        "output": '''import time
from typing import Dict

class WorkerWatchdog:
    """Tracks heartbeat timestamps of multiple worker threads."""
    def __init__(self, max_idle_sec: float = 10.0):
        self.max_idle = max_idle_sec
        self.heartbeats: Dict[str, float] = {}

    def ping(self, worker_id: str) -> None:
        self.heartbeats[worker_id] = time.time()

    def get_stale_workers(self) -> list[str]:
        now = time.time()
        return [w_id for w_id, ts in self.heartbeats.items() if now - ts > self.max_idle]''',
        "category": category
    })

    # 40. Async Polling Loop with Predicate
    tasks.append({
        "instruction": "Formulate an async polling utility that checks a predicate function at intervals until condition is met or timeout occurs.",
        "output": '''import asyncio
import time
from typing import Callable

async def poll_until(
    predicate_fn: Callable[[], bool],
    poll_interval_sec: float = 0.5,
    timeout_sec: float = 5.0
) -> bool:
    """Poll predicate_fn until it returns True or timeout_sec is exceeded."""
    start = time.time()
    while time.time() - start < timeout_sec:
        if predicate_fn():
            return True
        await asyncio.sleep(poll_interval_sec)
    return False''',
        "category": category
    })

    # 41. Multi-worker Map Reduce Thread Simulator
    tasks.append({
        "instruction": "Develop a multi-threaded MapReduce simulator using worker threads for mapping and a single reducer thread.",
        "output": '''from typing import Any, Callable, Dict, List
import queue
import threading

def threaded_map_reduce(
    data_chunks: List[List[Any]],
    mapper_fn: Callable[[Any], List[tuple[str, int]]],
    reducer_fn: Callable[[str, List[int]], Any]
) -> Dict[str, Any]:
    """Execute threaded map-reduce over partitioned data chunks."""
    intermediate_queue: queue.Queue = queue.Queue()

    def map_worker(chunk: List[Any]):
        for item in chunk:
            for k, v in mapper_fn(item):
                intermediate_queue.put((k, v))

    threads = [threading.Thread(target=map_worker, args=(c,)) for c in data_chunks]
    for t in threads: t.start()
    for t in threads: t.join()

    grouped: Dict[str, List[int]] = {}
    while not intermediate_queue.empty():
        k, v = intermediate_queue.get()
        grouped.setdefault(k, []).append(v)

    return {k: reducer_fn(k, vals) for k, vals in grouped.items()}''',
        "category": category
    })

    # 42. Async Event Throttle Decorator
    tasks.append({
        "instruction": "Design an async throttle decorator that ensures a coroutine is called at most once every interval seconds.",
        "output": '''import asyncio
import time
from typing import Any, Callable

def async_throttle(interval_sec: float):
    """Throttle coroutine calls to execute at most once per interval."""
    last_called = 0.0
    lock = asyncio.Lock()

    def decorator(fn: Callable[..., Any]):
        async def wrapper(*args, **kwargs) -> Any:
            nonlocal last_called
            async with lock:
                now = time.time()
                elapsed = now - last_called
                if elapsed < interval_sec:
                    await asyncio.sleep(interval_sec - elapsed)
                last_called = time.time()
                return await fn(*args, **kwargs)
        return wrapper
    return decorator''',
        "category": category
    })

    # 43. Thread-Safe Event Emitter
    tasks.append({
        "instruction": "Build a thread-safe Event Emitter supporting synchronized subscriber registration and event firing.",
        "output": '''import threading
from collections import defaultdict
from typing import Callable, Dict, List

class ThreadSafeEventEmitter:
    """Thread-safe event listener and dispatcher."""
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = defaultdict(list)
        self._lock = threading.Lock()

    def on(self, event: str, listener: Callable) -> None:
        with self._lock:
            self._listeners[event].append(listener)

    def emit(self, event: str, *args, **kwargs) -> None:
        with self._lock:
            listeners = list(self._listeners.get(event, []))
        for listener in listeners:
            listener(*args, **kwargs)''',
        "category": category
    })

    # 44. Async Worker Task Supervisor
    tasks.append({
        "instruction": "Construct an async task supervisor that monitors coroutine execution and restarts failed workers up to a limit.",
        "output": '''import asyncio
from typing import Callable

async def supervise_worker(coro_fn: Callable[[], Any], max_restarts: int = 3) -> None:
    """Run worker coroutine and restart upon unhandled exception up to max_restarts."""
    restarts = 0
    while restarts < max_restarts:
        try:
            await coro_fn()
            break
        except Exception:
            restarts += 1
            await asyncio.sleep(0.5)''',
        "category": category
    })

    # 45. Thread-Safe Reference Counter
    tasks.append({
        "instruction": "Write a thread-safe reference counting manager that tracks resource usage and releases upon zero references.",
        "output": '''import threading
from typing import Any, Callable

class RefCountedResource:
    """Resource wrapper triggering cleanup when reference count drops to zero."""
    def __init__(self, resource: Any, cleanup_fn: Callable[[Any], None]):
        self.resource = resource
        self.cleanup = cleanup_fn
        self.count = 1
        self.lock = threading.Lock()

    def retain(self) -> None:
        with self.lock:
            self.count += 1

    def release(self) -> None:
        with self.lock:
            self.count -= 1
            if self.count == 0:
                self.cleanup(self.resource)''',
        "category": category
    })

    # 46. Async Sleep Until Datetime Target
    tasks.append({
        "instruction": "Implement an async sleep helper that pauses execution until a target Unix timestamp is reached.",
        "output": '''import asyncio
import time

async def async_sleep_until_timestamp(target_timestamp: float) -> None:
    """Pause coroutine execution until target Unix timestamp."""
    delay = target_timestamp - time.time()
    if delay > 0:
        await asyncio.sleep(delay)''',
        "category": category
    })

    # 47. Async Concurrency Gate Token Dispenser
    tasks.append({
        "instruction": "Develop an async token dispenser limiting global concurrent operations across distributed callers.",
        "output": '''import asyncio

class AsyncConcurrencyGate:
    """Gate controller managing permission tokens for concurrent operations."""
    def __init__(self, total_tokens: int):
        self.sem = asyncio.Semaphore(total_tokens)

    async def enter(self) -> None:
        await self.sem.acquire()

    def exit(self) -> None:
        self.sem.release()''',
        "category": category
    })

    # 48. Thread-Safe LIFO Stack with Limit
    tasks.append({
        "instruction": "Create a bounded thread-safe LIFO stack that blocks on push when full and pop when empty.",
        "output": '''import threading
from typing import Any, List

class BoundedThreadStack:
    """Thread-safe bounded LIFO stack using condition variables."""
    def __init__(self, max_capacity: int):
        self.max_capacity = max_capacity
        self.items: List[Any] = []
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def push(self, val: Any) -> None:
        with self.cond:
            while len(self.items) >= self.max_capacity:
                self.cond.wait()
            self.items.append(val)
            self.cond.notify()

    def pop(self) -> Any:
        with self.cond:
            while not self.items:
                self.cond.wait()
            item = self.items.pop()
            self.cond.notify()
            return item''',
        "category": category
    })

    # 49. Async Connection Pool Simulator
    tasks.append({
        "instruction": "Build an async connection pool context manager managing connection acquisition and return.",
        "output": '''import asyncio
from typing import Any, List

class AsyncConnectionPool:
    """Asynchronous resource pool leasing items via context manager."""
    def __init__(self, connections: List[Any]):
        self.available: asyncio.Queue = asyncio.Queue()
        for conn in connections:
            self.available.put_nowait(conn)

    async def acquire(self) -> Any:
        return await self.available.get()

    def release(self, conn: Any) -> None:
        self.available.put_nowait(conn)''',
        "category": category
    })

    # 50. Threaded Batch Flush Queue
    tasks.append({
        "instruction": "Design a multithreaded queue that flushes batches of items periodically or upon reaching capacity.",
        "output": '''import queue
import threading
from typing import Any, Callable, List

class ThreadedBatchFlusher:
    """Aggregates items and flushes batches to a callback."""
    def __init__(self, batch_size: int, callback: Callable[[List[Any]], None]):
        self.batch_size = batch_size
        self.callback = callback
        self.items: List[Any] = []
        self.lock = threading.Lock()

    def add(self, item: Any) -> None:
        with self.lock:
            self.items.append(item)
            if len(self.items) >= self.batch_size:
                batch = list(self.items)
                self.items.clear()
                self.callback(batch)''',
        "category": category
    })

    # 51. Async Event Multiplexer
    tasks.append({
        "instruction": "Formulate an async multiplexer combining notifications from multiple asyncio.Event triggers into one.",
        "output": '''import asyncio
from typing import List

async def wait_any_event(events: List[asyncio.Event]) -> int:
    """Return index of the first asyncio.Event that gets set."""
    tasks = [asyncio.create_task(ev.wait()) for ev in events]
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
    for p in pending:
        p.cancel()
    first_task = done.pop()
    return tasks.index(first_task)''',
        "category": category
    })

    # 52. Async Multi-producer Single-consumer (MPSC)
    tasks.append({
        "instruction": "Implement an MPSC (Multi-Producer Single-Consumer) async channel wrapper with producer tracking.",
        "output": '''import asyncio
from typing import Any

class AsyncMPSCChannel:
    """Multi-producer single-consumer channel tracking registered producers."""
    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.active_producers = 0

    def register_producer(self) -> None:
        self.active_producers += 1

    async def send(self, message: Any) -> None:
        await self.queue.put(message)

    async def producer_done(self) -> None:
        self.active_producers -= 1
        if self.active_producers == 0:
            await self.queue.put(None)  # Terminate consumer''',
        "category": category
    })

    # 53. Async Pipeline Stage Filter
    tasks.append({
        "instruction": "Develop an async transformer function filtering and mapping items from an input queue to an output queue.",
        "output": '''import asyncio
from typing import Any, Callable

async def async_filter_map_stage(
    in_q: asyncio.Queue,
    out_q: asyncio.Queue,
    transform_fn: Callable[[Any], Any],
    predicate_fn: Callable[[Any], bool]
) -> None:
    """Read items from in_q, apply transform and predicate, and write to out_q."""
    while True:
        item = await in_q.get()
        if item is None:
            await out_q.put(None)
            break
        if predicate_fn(item):
            transformed = await transform_fn(item)
            await out_q.put(transformed)''',
        "category": category
    })

    # 54. Thread-Safe Bounded Stack with Timeout
    tasks.append({
        "instruction": "Create a thread-safe stack with timed push and pop operations using threading.Condition.",
        "output": '''import threading
import time
from typing import Any, List, Optional

class TimedThreadStack:
    """Thread-safe stack with timeout support for push and pop."""
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Any] = []
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def push(self, val: Any, timeout: float) -> bool:
        with self.cond:
            start = time.time()
            while len(self.items) >= self.capacity:
                rem = timeout - (time.time() - start)
                if rem <= 0 or not self.cond.wait(timeout=rem):
                    return False
            self.items.append(val)
            self.cond.notify()
            return True''',
        "category": category
    })

    # 55. Async Countdown Deadline Timer
    tasks.append({
        "instruction": "Write an async countdown timer that fires a callback coroutine if not cancelled before expiration.",
        "output": '''import asyncio
from typing import Callable

class AsyncDeadlineTimer:
    """Executes callback when deadline expires unless cancelled."""
    def __init__(self, timeout_sec: float, callback: Callable[[], Any]):
        self.timeout = timeout_sec
        self.callback = callback
        self.task: asyncio.Task = asyncio.create_task(self._run())

    async def _run(self) -> None:
        try:
            await asyncio.sleep(self.timeout)
            await self.callback()
        except asyncio.CancelledError:
            pass

    def cancel(self) -> None:
        self.task.cancel()''',
        "category": category
    })

    # 56. Thread Worker Pool with Dynamic Worker Scaling
    tasks.append({
        "instruction": "Construct a thread pool manager that tracks active worker thread count.",
        "output": '''import threading
from typing import List

class SimpleWorkerPool:
    """Manages active thread lifecycles."""
    def __init__(self):
        self.workers: List[threading.Thread] = []
        self.lock = threading.Lock()

    def spawn(self, target_fn, *args) -> threading.Thread:
        t = threading.Thread(target=target_fn, args=args)
        with self.lock:
            self.workers.append(t)
        t.start()
        return t

    def active_count(self) -> int:
        with self.lock:
            self.workers = [t for t in self.workers if t.is_alive()]
            return len(self.workers)''',
        "category": category
    })

    # 57. Async Burst Token Bucket
    tasks.append({
        "instruction": "Design an async token bucket that allows instantaneous burst capacity above normal replenishment rates.",
        "output": '''import asyncio
import time

class BurstTokenBucket:
    """Async token bucket supporting burst allowances."""
    def __init__(self, burst_capacity: float, steady_rate: float):
        self.capacity = burst_capacity
        self.rate = steady_rate
        self.tokens = burst_capacity
        self.last_check = time.time()
        self.lock = asyncio.Lock()

    async def take(self, count: float = 1.0) -> bool:
        async with self.lock:
            now = time.time()
            self.tokens = min(self.capacity, self.tokens + (now - self.last_check) * self.rate)
            self.last_check = now
            if self.tokens >= count:
                self.tokens -= count
                return True
            return False''',
        "category": category
    })

    # 58. Thread-Safe Latch Primitive
    tasks.append({
        "instruction": "Build a CountDownLatch concurrency primitive counting down from N to 0 in Python multithreading.",
        "output": '''import threading

class CountDownLatch:
    """Synchronizes threads by counting down from N to zero."""
    def __init__(self, count: int):
        self.count = count
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

    def count_down(self) -> None:
        with self.cond:
            if self.count > 0:
                self.count -= 1
                if self.count == 0:
                    self.cond.notify_all()

    def wait(self) -> None:
        with self.cond:
            while self.count > 0:
                self.cond.wait()''',
        "category": category
    })

    # 59. Async Distributed Lock Lease Simulator
    tasks.append({
        "instruction": "Formulate an async lock lease simulator with automatic expiration and heartbeat renewal.",
        "output": '''import asyncio
import time

class AsyncLockLease:
    """Simulates a lease-based distributed lock with TTL expiration."""
    def __init__(self, ttl_sec: float = 10.0):
        self.ttl = ttl_sec
        self.expires_at = 0.0
        self.holder: str = ""

    def acquire(self, client_id: str) -> bool:
        now = time.time()
        if now > self.expires_at or self.holder == client_id:
            self.holder = client_id
            self.expires_at = now + self.ttl
            return True
        return False

    def renew(self, client_id: str) -> bool:
        if self.holder == client_id and time.time() <= self.expires_at:
            self.expires_at = time.time() + self.ttl
            return True
        return False''',
        "category": category
    })

    # 60. Thread-Safe Read-Write Granular Map
    tasks.append({
        "instruction": "Implement a partitioned thread-safe dictionary using multiple bucket locks to reduce lock contention.",
        "output": '''import threading
from typing import Any, Dict, List, Optional

class PartitionedThreadMap:
    """Thread-safe hash map with sharded locks for reduced contention."""
    def __init__(self, num_shards: int = 16):
        self.num_shards = num_shards
        self.shards: List[Dict[str, Any]] = [{} for _ in range(num_shards)]
        self.locks: List[threading.Lock] = [threading.Lock() for _ in range(num_shards)]

    def _shard_idx(self, key: str) -> int:
        return hash(key) % self.num_shards

    def set(self, key: str, val: Any) -> None:
        idx = self._shard_idx(key)
        with self.locks[idx]:
            self.shards[idx][key] = val

    def get(self, key: str) -> Optional[Any]:
        idx = self._shard_idx(key)
        with self.locks[idx]:
            return self.shards[idx].get(key)''',
        "category": category
    })

    return tasks
