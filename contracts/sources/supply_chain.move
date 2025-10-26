module supply_chain::supply_chain {
    use sui::object::{Self, UID};
    use sui::transfer;
    use sui::tx_context::{Self, TxContext};
    use std::string::{Self, String};
    use sui::clock::{Self, Clock};
    use sui::event;

    /// Struct representing a shipment with AI-generated analysis
    struct Shipment has key, store {
        id: UID,
        shipment_id: String,
        ai_summary: String,
        confidence_score: u64,
        timestamp: u64,
        oracle_signature: vector<u8>,
        oracle_address: address,
    }

    /// Registry to store and lookup shipments
    struct ShipmentRegistry has key {
        id: UID,
        owner: address,
    }

    /// Event emitted when a shipment is updated
    struct ShipmentUpdated has copy, drop {
        shipment_id: String,
        confidence_score: u64,
        timestamp: u64,
        oracle_address: address,
    }

    /// Event emitted when a new shipment is created
    struct ShipmentCreated has copy, drop {
        shipment_id: String,
        timestamp: u64,
    }

    /// Error codes
    const EInvalidConfidenceScore: u64 = 1;
    const EInvalidSignature: u64 = 2;
    const EUnauthorized: u64 = 3;

    /// Initialize the module - creates the registry
    fun init(ctx: &mut TxContext) {
        let registry = ShipmentRegistry {
            id: object::new(ctx),
            owner: tx_context::sender(ctx),
        };
        transfer::share_object(registry);
    }

    /// Oracle function to create or update a shipment record
    /// This is called by the off-chain oracle after generating AI analysis
    public entry fun oracle_update(
        shipment_id: vector<u8>,
        ai_summary: vector<u8>,
        confidence_score: u64,
        oracle_signature: vector<u8>,
        clock: &Clock,
        ctx: &mut TxContext
    ) {
        // Validate confidence score is in valid range (0-100)
        assert!(confidence_score <= 100, EInvalidConfidenceScore);

        // Convert vectors to strings
        let shipment_id_str = string::utf8(shipment_id);
        let ai_summary_str = string::utf8(ai_summary);

        // Get current timestamp
        let timestamp = clock::timestamp_ms(clock);

        // Get oracle address
        let oracle_addr = tx_context::sender(ctx);

        // Create shipment object
        let shipment = Shipment {
            id: object::new(ctx),
            shipment_id: shipment_id_str,
            ai_summary: ai_summary_str,
            confidence_score,
            timestamp,
            oracle_signature,
            oracle_address: oracle_addr,
        };

        // Emit update event
        event::emit(ShipmentUpdated {
            shipment_id: shipment_id_str,
            confidence_score,
            timestamp,
            oracle_address: oracle_addr,
        });

        // Transfer shipment to sender (could also be shared or frozen)
        transfer::transfer(shipment, oracle_addr);
    }

    /// Create a new shipment record (for testing or manual creation)
    public entry fun create_shipment(
        shipment_id: vector<u8>,
        ai_summary: vector<u8>,
        confidence_score: u64,
        clock: &Clock,
        ctx: &mut TxContext
    ) {
        assert!(confidence_score <= 100, EInvalidConfidenceScore);

        let shipment_id_str = string::utf8(shipment_id);
        let ai_summary_str = string::utf8(ai_summary);
        let timestamp = clock::timestamp_ms(clock);
        let creator = tx_context::sender(ctx);

        let shipment = Shipment {
            id: object::new(ctx),
            shipment_id: shipment_id_str,
            ai_summary: ai_summary_str,
            confidence_score,
            timestamp,
            oracle_signature: vector::empty(),
            oracle_address: creator,
        };

        event::emit(ShipmentCreated {
            shipment_id: shipment_id_str,
            timestamp,
        });

        transfer::transfer(shipment, creator);
    }

    /// Update an existing shipment (requires ownership)
    public entry fun update_shipment(
        shipment: &mut Shipment,
        new_summary: vector<u8>,
        new_confidence: u64,
        new_signature: vector<u8>,
        clock: &Clock,
        ctx: &mut TxContext
    ) {
        assert!(new_confidence <= 100, EInvalidConfidenceScore);

        // Update fields
        shipment.ai_summary = string::utf8(new_summary);
        shipment.confidence_score = new_confidence;
        shipment.timestamp = clock::timestamp_ms(clock);
        shipment.oracle_signature = new_signature;
        shipment.oracle_address = tx_context::sender(ctx);

        // Emit event
        event::emit(ShipmentUpdated {
            shipment_id: shipment.shipment_id,
            confidence_score: new_confidence,
            timestamp: shipment.timestamp,
            oracle_address: shipment.oracle_address,
        });
    }

    /// Get shipment details (accessor functions for frontend)
    public fun get_shipment_id(shipment: &Shipment): String {
        shipment.shipment_id
    }

    public fun get_ai_summary(shipment: &Shipment): String {
        shipment.ai_summary
    }

    public fun get_confidence_score(shipment: &Shipment): u64 {
        shipment.confidence_score
    }

    public fun get_timestamp(shipment: &Shipment): u64 {
        shipment.timestamp
    }

    public fun get_oracle_address(shipment: &Shipment): address {
        shipment.oracle_address
    }

    public fun get_signature_length(shipment: &Shipment): u64 {
        vector::length(&shipment.oracle_signature)
    }

    #[test_only]
    /// Test helper function
    public fun init_for_testing(ctx: &mut TxContext) {
        init(ctx);
    }
}