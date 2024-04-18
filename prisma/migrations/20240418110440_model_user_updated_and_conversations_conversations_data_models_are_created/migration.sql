-- CreateTable
CREATE TABLE "hb_conversations" (
    "id" SERIAL NOT NULL,
    "conversation_id" INTEGER NOT NULL,
    "conversation_name" TEXT NOT NULL,
    "user_id" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP(3),

    CONSTRAINT "hb_conversations_pkey" PRIMARY KEY ("conversation_id")
);

-- CreateTable
CREATE TABLE "hb_coversations_data" (
    "cd_id" SERIAL NOT NULL,
    "cd_question" TEXT,
    "cd_response" TEXT,
    "conversation_id" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP(3)
);

-- CreateIndex
CREATE UNIQUE INDEX "hb_conversations_conversation_id_key" ON "hb_conversations"("conversation_id");

-- CreateIndex
CREATE UNIQUE INDEX "hb_coversations_data_cd_id_key" ON "hb_coversations_data"("cd_id");

-- AddForeignKey
ALTER TABLE "hb_conversations" ADD CONSTRAINT "hb_conversations_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "hb_users"("user_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "hb_coversations_data" ADD CONSTRAINT "hb_coversations_data_conversation_id_fkey" FOREIGN KEY ("conversation_id") REFERENCES "hb_conversations"("conversation_id") ON DELETE RESTRICT ON UPDATE CASCADE;
